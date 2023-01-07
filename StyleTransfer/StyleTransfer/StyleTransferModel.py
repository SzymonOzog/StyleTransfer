import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class StyleTransferModel():
    def __init__(self, content_image, style_image):
        super(StyleTransferModel, self).__init__()
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'vgg19', pretrained=True).features
        self.model.eval()
        self.model.to(device)

        size = 512 if device == "cuda" else 128
        self.content_image = cv2.resize(content_image, (size, size)) / 255.0
        self.style_image = cv2.resize(style_image, (size, size)) / 255.0
        
        self.content_loss_weight = 1e0
        self.style_loss_weight = 1e7

        self.content_image = content_image.copy()
        self.style_image = style_image.copy()
        
        self.cnn_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
        self.cnn_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
        
        self.activation = {}

        def get_activation(name=None, m=None):
            def hook(model, input, output):
                m.activation[name] = output
            return hook


        self.model[22].register_forward_hook(get_activation("content", self))
        self.model[1].register_forward_hook(get_activation("style1", self))
        self.model[11].register_forward_hook(get_activation("style2", self))
        self.model[19].register_forward_hook(get_activation("style3", self))
        self.model[29].register_forward_hook(get_activation("style4", self))
        
    def transfer_image(self, iters):
        self.content_image = torch.tensor(self.content_image, requires_grad=True).permute(2, 0, 1).unsqueeze(0).float().to(device)
        self.content_image.retain_grad()
        self.style_image = torch.tensor(self.style_image).permute(2, 0, 1).unsqueeze(0).float().to(device)

        def gram_matrix(input):
            a, b, c, d = input.size()
            features = input.view(a * b, c * d)  # resise F_XL into \hat F_XL
            G = torch.mm(features, features.t())  # compute the gram product
            return G.div(a * b * c * d)

        optimizer = torch.optim.Adam([self.content_image], lr = 0.05)
        for j in range(iters):
            optimizer.zero_grad()

            self.model((self.style_image - self.cnn_mean.view(3, 1, 1)) / self.cnn_std.view(3, 1, 1))
            content_target = self.activation["content"]
            style_target = [self.activation["style1"], self.activation["style2"], self.activation["style3"], self.activation["style4"]]

            

            self.model((self.content_image - self.cnn_mean.view(3, 1, 1)) / self.cnn_std.view(3, 1, 1))
            content = self.activation["content"]
            style = [self.activation["style1"], self.activation["style2"], self.activation["style3"], self.activation["style4"]]

            content_loss = F.mse_loss(content, content_target) * self.content_loss_weight
            style_loss = 0
            for i in range(len(style)):
                style_loss += F.mse_loss(gram_matrix(style[i]), gram_matrix(style_target[i])) * self.style_loss_weight
            
            loss = content_loss + style_loss
            loss.backward()
            if j % 10 == 0:
                print("Iteration: ", j, "Loss: ", loss.item(), "Content loss: ", content_loss.item(), "Style loss: ", style_loss.item())
            optimizer.step()
            with torch.no_grad():
                self.content_image.clamp_(0, 1)
        return self.content_image[0].permute(1, 2, 0).detach().cpu().numpy()
        
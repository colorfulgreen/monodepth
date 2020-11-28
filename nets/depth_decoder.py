import torch.nn as nn
import torch.nn.functional as F


def upconv(in_planes, out_planes):
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=(3, 3), stride=(1,1)),
        nn.ELU(alpha=1.0, inplace=True)
    )


def predict_disp(in_planes):
    return nn.Sequential(
        nn.Conv2d(in_planes, 1, kernel_size=3, padding=1),
        nn.Sigmoid()
    )


def upsample(x):
    return F.interpolate(x, scale_factor=2, mode='nearest')


class DepthDecoder(nn.Module):

    def __init__(self):
        super(DepthDecoder, self).__init__()

        n_planes = [512, 256, 128, 64, 32, 16]

        self.upconv4 = upconv(n_planes[0], n_planes[1])
        self.upconv3 = upconv(n_planes[1], n_planes[2])
        self.upconv2 = upconv(n_planes[2], n_planes[3])
        self.upconv1 = upconv(n_planes[3], n_planes[4])
        self.upconv0 = upconv(n_planes[4], n_planes[5])

        self.iconv4 = upconv(n_planes[1], n_planes[1])
        self.iconv3 = upconv(n_planes[2], n_planes[2])
        self.iconv2 = upconv(n_planes[3], n_planes[3])
        self.iconv1 = upconv(n_planes[4], n_planes[4])
        self.iconv0 = upconv(n_planes[5], n_planes[5])

        self.disp3 = predict_disp(n_planes[2])
        self.disp2 = predict_disp(n_planes[3])
        self.disp1 = predict_disp(n_planes[4])
        self.disp0 = predict_disp(n_planes[5])

    def forward(self, encode_features):
        x = encoded_features[-1]

        out_upconv4 = self.upconv4(x)
        out_upsample4 = upsample(out_upconv4)
        concat4 = torch.cat(out_upsample4, encode_features[4])
        out_iconv4 = self.iconv4(concat4)

        out_upconv3 = self.upconv3(x)
        out_upsample3 = upsample(out_upconv3)
        concat3 = torch.cat(out_upsample3, encode_features[3])
        out_iconv3 = self.iconv4(concat3)
        disp3 = self.disp3(out_iconv3)

        out_upconv2 = self.upconv2(x)
        out_upsample2 = upsample(out_upconv2)
        concat2 = torch.cat(out_upsample2, encode_features[2])
        out_iconv2 = self.iconv2(concat2)
        disp2 = self.disp2(out_iconv2)

        out_upconv1 = self.upconv1(x)
        out_upsample1 = upsample(out_upconv1)
        concat1 = torch.cat(out_upsample1, encode_features[1])
        out_iconv1 = self.iconv1(concat1)
        disp1 = self.disp1(out_iconv1)

        out_upconv0 = self.upconv0(x)
        out_upsample0 = upsample(out_upconv0)
        concat0 = torch.cat(out_upsample0, encode_features[0])
        out_iconv0 = self.iconv0(concat0)
        disp0 = self.disp0(out_iconv0)

        return [disp3, disp2, disp1, disp0]

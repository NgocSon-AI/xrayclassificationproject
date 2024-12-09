import os
import torch
import streamlit as st
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path


def save_image(uploaded_file):
    if uploaded_file is not None:
        save_path = os.path.join("image","input.png")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Image save to {save_path}")

        model = torch.load(Path('model/model.pt'))

        transform = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])

        image = Image.open(Path('image/input.png'))

        input_tensor = transform(image)

        input_tensor = input_tensor.view(1, 1, 224, 224).repeat(1, 3, 1, 1)
        input_tensor = input_tensor.to('cuda')
        output = model(input_tensor)
        output_cpu = output.data.cpu()
        prediction = int(torch.max(output_cpu, 1)[1].numpy())
        
        print(prediction)

        if(prediction == 0):
            print('Normal')
            st.text_area(label="Prediction", value="NORMAL", height=100)
        if(prediction == 1):
            print('PNEUMONIA')
            st.text_area(label="Prediction: ", value="PNEUMONIA", height=100)


if __name__ == "__main__":
    st.title("Xray lung classifier")
    uploaded_file = st.file_uploader("Uploade an image", type=["jpg","png","jepg"])
    save_image(uploaded_file=uploaded_file)
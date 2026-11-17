# 56 — OFFICIAL ComfyUI Wan2.2 Fun Control tutorial capture (primary source)
# URL: https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control
# Fetched 2026-11-15 via playwright (container browser).
#
# VERIFIED KEY FACTS:
# - Wan2.2-Fun-Control: Alibaba PAI, Apache 2.0, commercial use OK.
# - Controls: Canny, Depth, OpenPose, MLSD, trajectory.
# - Models: wan2.2_fun_control_high/low_noise_14B_fp8_scaled.safetensors
#   + wan2.2_i2v_lightx2v_4steps_lora_v1_high/low_noise.safetensors
#   + umt5_xxl_fp8_e4m3fn_scaled.safetensors + wan_2.1_vae.safetensors
# - LoRA pairing rule: high-noise model ONLY with high-noise LoRA (LoraLoaderModelOnly), low likewise.
# - Measured RTX 4090D 24GB @ 640x640 81 frames: fp8 ~524s/520s; fp8+4-step LoRA ~138s first / 79s after.
#   4-step LoRA enabled by default (Ctrl+B toggles the non-LoRA variant); some dynamics loss.
# - Preprocessed control video loads into the second Load Video node directly.
#
# FULL PAGE TEXT:

Documentation Index

Fetch the complete documentation index at: /llms.txt

Use this file to discover all available pages before exploring further.

Skip to main content
ComfyUI home page
English
Search Comfy documentation...
Ctrl K
Blog
Pricing
Platform
Download
Comfy Cloud
Getting started
Tutorials
Comfy Router
Agent tools
Built-in Nodes
Developer
Support
Basic Concepts
Workflows
Nodes
Custom Nodes
Properties
Links
Models
Dependencies
Interface Guide
Interface Overview
Workspace
Feature components
ComfyUI Settings
Account & credits
Cloud Exclusive
Tutorials
Basic Examples
ControlNet
Image
3D
LLM
Video
MiniMax H3
Pika
LTX
Wan Video
Wan Animate 2
Wan2.2
Wan2.2 Animate
Wan Dancer
Wan2.2 S2V
Wan2.2 Fun Inp
Wan2.2 Fun Control
Wan2.2 Fun Camera
Wan2.1
ByteDance
Hunyuan
Cosmos
Kandinsky
ZAI
Audio
Utility
Comfy Cloud Nodes
Overview
Partner Nodes
Overview
Pricing
Concurrency Limits
FAQs
Data Retention
Model Providers
Partner Models
On this page
ComfyOrg Wan2.2 Fun InP & Control Youtube Live Stream Replay
Wan2.2 Fun Control Video Generation Workflow Example
1. Download Workflow and Materials
2. Models
3. Workflow Guide
Additional Notes
Wan Video
Wan2.2 Fun Control in ComfyUI: Control-Video Generation
Copy page

Run the Wan2.2 Fun Control 14B workflow in ComfyUI to generate video guided by a control video, with high and low noise models and 4-step LoRAs.

Wan2.2-Fun-Control is a next-generation video generation and control model launched by Alibaba PAI team. Through innovative Control Codes mechanism combined with deep learning and multi-modal conditional inputs, it can generate high-quality videos that comply with preset control conditions. The model is released under the Apache 2.0 license and supports commercial use.
Key Features:
Multi-modal Control: Supports multiple control conditions including Canny (line art), Depth, OpenPose (human pose), MLSD (geometric edges), and trajectory control
High-Quality Video Generation: Based on the Wan2.2 architecture, outputs film-level quality videos
Multi-language Support: Supports multi-language prompts including Chinese and English
Below are the relevant model weights and code repositories:
🤗Wan2.2-Fun-A14B-Control
Code repository: VideoX-Fun
ComfyOrg Wan2.2 Fun InP & Control Youtube Live Stream Replay
Wan2.2 Fun Control Video Generation Workflow Example
Local users
Cloud users
Make sure your ComfyUI is updated.
Download ComfyUI
Update Guide
Workflows in this guide can be found in the Workflow Templates. If you can’t find them in the template, your ComfyUI may be outdated.
If nodes are missing when loading a workflow, possible reasons:
You are not using the latest ComfyUI version (Nightly version)
Some nodes failed to import at startup
This workflow provides two versions:
A version using Wan2.2-Lightning 4-step LoRA from lightx2v: may cause some loss in video dynamics but offers faster speed
A fp8_scaled version without acceleration LoRA
Below are the test results using an RTX4090D 24GB VRAM GPU at 640×640 resolution with 81 frames
Model Type	VRAM Usage	First Generation Time	Second Generation Time
fp8_scaled	83%	≈ 524s	≈ 520s
fp8_scaled + 4-step LoRA	89%	≈ 138s	≈ 79s
Since using the 4-step LoRA provides a better experience for first-time workflow users, but may cause some loss in video dynamics, we have enabled the accelerated LoRA version by default. If you want to enable the other workflow, select it and use Ctrl+B to activate.
1. Download Workflow and Materials
Update your ComfyUI to the latest version, then download and drag the workflow file into ComfyUI, or find “Wan2.2 Fun Control” in the Template Library under Workflow → Browse Templates → Video.
Run on Comfy Cloud
Open in Comfy Cloud
Download Workflow
Download JSON or search “Wan2.2 Fun Control” in Template Library
Please download the following images and videos as input materials.
Input materials
video_wan2_2_14B_fun_control_start_image.jpg
Start frame for video generation. Download and use this image, or replace with your own.
video_wan2_2_14B_fun_control_start_image_control_video.mp4
Preprocessed pose control video. Download and use this video, or replace with your own.
We use a preprocessed video here.
2. Models
All models involved in this guide can be found here.
Diffusion Models
Wan2.2 Fun Control High Noise 14B FP8
wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors: High noise diffusion model
Wan2.2 Fun Control Low Noise 14B FP8
wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors: Low noise diffusion model
Wan2.2-Lightning LoRA (Optional, for acceleration)
High Noise 4-Step LoRA
wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors: High noise 4-step acceleration LoRA
Low Noise 4-Step LoRA
wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors: Low noise 4-step acceleration LoRA
VAE
Wan2.1 VAE
wan_2.1_vae.safetensors: Wan2.1 VAE for encoding/decoding
Text Encoder
UMT5 XXL FP8 Scaled
umt5_xxl_fp8_e4m3fn_scaled.safetensors: Scaled FP8 text encoder
ComfyUI/
├───📂 models/
│   ├───📂 diffusion_models/
│   │   ├─── wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors
│   │   └─── wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors
│   ├───📂 loras/
│   │   ├─── wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors
│   │   └─── wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors
│   ├───📂 text_encoders/
│   │   └─── umt5_xxl_fp8_e4m3fn_scaled.safetensors 
│   └───📂 vae/
│       └── wan_2.1_vae.safetensors

3. Workflow Guide
This workflow uses LoRA. Please ensure the corresponding Diffusion model and LoRA are matched: high noise and low noise models and LoRAs need to be used correspondingly.
High noise model and LoRA loading
Ensure the Load Diffusion Model node loads the wan2.2_fun_control_high_noise_14B_fp8_scaled.safetensors model
Ensure the LoraLoaderModelOnly node loads the wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors
Low noise model and LoRA loading
Ensure the Load Diffusion Model node loads the wan2.2_fun_control_low_noise_14B_fp8_scaled.safetensors model
Ensure the LoraLoaderModelOnly node loads the wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors
Ensure the Load CLIP node loads the umt5_xxl_fp8_e4m3fn_scaled.safetensors model
Ensure the Load VAE node loads the wan_2.1_vae.safetensors model
Upload the start frame in the Load Image node
In the second Load video node, load the pose control video. The provided video has been preprocessed and can be used directly
Since we provide a preprocessed pose video, the corresponding video image preprocessing node needs to be disabled. You can select it and use Ctrl + B to disable it
Modify the Prompt: you can use both Chinese and English
In Wan22FunControlToVideo, modify the video dimensions. The default is set to 640×640 resolution to avoid excessive processing time for users with low VRAM
Click the Run button, or use the shortcut Ctrl(cmd) + Enter to execute video generation
Additional Notes
Since ComfyUI’s built-in nodes only include Canny preprocessor, you can use tools like ComfyUI-comfyui_controlnet_aux to implement other types of image preprocessing
💬
💬 Click or scroll here to load comments

Was this page helpful?

Yes
No
Suggest edits
Raise issue
Wan2.2 Fun Inp
Wan2.2 Fun Camera
ComfyUI home page

Resources

installation
Tutorials
Development

Products

Features
Gallery
Download

Company

About
Careers
Terms of Service
Privacy Policy
github
x
discord
youtube
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform

import cv2
import time
import torch
import asyncio
import argparse
import numpy as np
import time
import datetime

from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.plots import output_to_keypoint, plot_skeleton_kpts
from utils.general import non_max_suppression_kpt, strip_optimizer
from torchvision import transforms

from isup import isUpR
from isup import isUpL
from isup import Torso
from nats_client import publish 

@torch.no_grad()
async def run(poseweights= 'yolov7-w6-pose.pt', source='pose.mp4', device='cpu'):
    rightArmFlag = False
    leftArmFlag = False
    bothArmsFlag = False

    path = source
    ext = path.split('/')[-1].split('.')[-1].strip().lower()
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    
    detection_stopped_time = None
    timer_started = False
    detection = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 15

    if ext in ["mp4", "webm", "avi"] or ext not in ["mp4", "webm", "avi"] and ext.isnumeric():
        input_path = int(path) if path.isnumeric() else path
        device = select_device(opt.device)
        half = device.type != 'cpu'
        model = attempt_load(poseweights, map_location=device)
        _ = model.eval()

        cap = cv2.VideoCapture(input_path)

        

        if (cap.isOpened() == False):
            print('Error while trying to read video. Please check path again')
        frame_size= (int(cap.get(3)), int(cap.get(4)))
        frame_width, frame_height = int(cap.get(3)), int(cap.get(4))

        vid_write_image = letterbox(
            cap.read()[1], (frame_width), stride=64, auto=True)[0]
        resize_height, resize_width = vid_write_image.shape[:2]
        out_video_name = "output" if path.isnumeric else f"{input_path.split('/')[-1].split('.')[0]}"
        #out = cv2.VideoWriter(f"{out_video_name}_result4.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (resize_width, resize_height))

        frame_count, total_fps = 0, 0

        while cap.isOpened:
            
           
           # print(f"Frame {frame_count} Processing")
            ret, frame = cap.read()
            
            if ret:
                
                orig_image = frame
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  
                # preprocess image
                image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
                image = letterbox(image, (frame_width), stride=64, auto=True)[0]
                image_ = image.copy()
                image = transforms.ToTensor()(image)
                image = torch.tensor(np.array([image.numpy()]))

                image = image.to(device)
                image = image.float()
                start_time = time.time()

                with torch.no_grad():
                    output, _ = model(image)

                output = non_max_suppression_kpt(output, 0.25, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)
                output = output_to_keypoint(output)
                img = image[0].permute(1, 2, 0) * 255
                img = img.cpu().numpy().astype(np.uint8)

                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                icon = cv2.imread("botao-x.png")
                thre = (frame_height//2)+100
                
                

                

                for idx in range(output.shape[0]):
                    kpts = output[idx, 7:].T
                    #plot_skeleton_kpts(img,kpts,3)
                    xmin, ymin = (output[idx,2] - output[idx,4]/2), (output[idx,3] - output[idx,5]/2)
                    xmax, ymax = (output[idx,2] + output[idx,4]/2), (output[idx,3] + output[idx,5]/2)
                    p5 = (int(xmin), int(ymin))
                    p6 = (int(xmax), int(ymax))
                    dx = int(xmax) - int(xmin)
                    dy = int(ymax) - int(ymin)
                    cx = int(xmin + xmax)//2
                    cy = int(ymin + ymax)//2
                    icon = cv2.resize(icon, (50,50), interpolation=cv2.INTER_LINEAR)
                    difference = dy - dx 
                    # ph = Get_coord(kpts, 2)
                    Lup = isUpL(img, kpts, 5, 7, 9, draw=True)
                    Rup = isUpR(img, kpts, 6, 8, 10, draw=True)
                    Torso1 = Torso(img, kpts, 6 , 5, 11, 12, draw=True)
                   # print(difference)
                   # print(dy)
                   # print(dx)
                    bothUp: bool = Rup == True and Lup == True
                    
                    # and (int(ph)> thre))
                    
                    if difference < 50:
                        if detection:
                            timer_started = False
                        else:
                            detection = True
                            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%S")
                            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 24, frame_size)
                            print("******************COMECOU A GRAVAR*******************")
                    elif detection:
                        if timer_started:
                            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                                detection = False
                                timer_started = False
                                out.release()
                                print("################# PAROU DE GRAVAR ####################")
                        else:
                            timer_started = True
                            detection_stopped_time = time.time()
                    
                    if detection:
                        out.write(frame)
                    
                    if ((difference<0) or (difference < 0)):
                           # font
                        font = cv2.FONT_HERSHEY_COMPLEX
                        
                        # org
                        org = (50, 50)
                        
                        # fontScale
                        fontScale = 1
                        
                        # Blue color in BGR
                        color = (0, 0, 0)
                        
                        # Line thickness of 2 px
                        thickness = 2
                        
                        cv2.putText(img, 'Caiu vovo', org, font, 
                                        fontScale, color, thickness, cv2.LINE_AA)
                        img[cy:cy+50, cx:cx+50] = icon
                        
                      
          
                    if bothUp:
                        # font
                        font = cv2.FONT_HERSHEY_COMPLEX
                        
                        # org
                        org = (50, 50)
                        
                        # fontScale
                        fontScale = 1
                        
                        # Blue color in BGR
                        color = (0, 0, 0)
                        
                        # Line thickness of 2 px
                        thickness = 2
                        
                        # Using cv2.putText() method
                        image = cv2.putText(img, 'Dois bracos levantados', org, font, 
                                        fontScale, color, thickness, cv2.LINE_AA)
                        
                        if (not bothArmsFlag):
                            print('both_up')
                            bothArmsFlag = True
                            await publish('BOTH')

                    else:    
                        if Lup == True:
                            # font
                            font = cv2.FONT_HERSHEY_COMPLEX
                            
                            # org
                            org = (50, 50)
                            
                            # fontScale
                            fontScale = 1
                            
                            # Blue color in BGR
                            color = (0, 0, 0)
                            
                            # Line thickness of 2 px
                            thickness = 2
                            
                            # Using cv2.putText() method
                            image = cv2.putText(img, 'Braco esquerdo levantado', org, font, 
                                            fontScale, color, thickness, cv2.LINE_AA)
                            
                            if (not leftArmFlag):
                                print('left_up')
                                leftArmFlag = True
                                await publish('LEFT')

                        else:
                            if Rup == True:
                                # font
                                font = cv2.FONT_HERSHEY_COMPLEX
                                
                                # org
                                org = (50, 50)
                                
                                # fontScale
                                fontScale = 1
                                
                                # Blue color in BGR
                                color = (0, 0, 0)
                                
                                # Line thickness of 2 px
                                thickness = 2
                                
                                # Using cv2.putText() method
                                image = cv2.putText(img, 'Braco direito levantado', org, font, 
                                                fontScale, color, thickness, cv2.LINE_AA)
                                
                                if (not rightArmFlag):
                                    print('both_up')
                                    rightArmFlag = True
                                    await publish('RIGHT')

                    if (bothUp != bothArmsFlag): 
                        bothArmsFlag = bothUp

                    if (Rup != rightArmFlag): 
                        rightArmFlag = Rup

                    if (Lup != leftArmFlag): 
                        leftArmFlag = Lup

                if ext.isnumeric():
                    cv2.imshow("Detection", img)
                    key = cv2.waitKey(1)
                    if key == ord('c'):
                        break

                end_time = time.time()
                fps = 1 / (end_time - start_time)
                total_fps += fps
                frame_count += 1
                #out.write(img)
            else:
                break
        out.release()        
        cap.release()
        avg_fps = total_fps / frame_count
        print(f"Average FPS: {avg_fps:.3f}")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str, help='path to video or 0 for webcam')
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')
    opt = parser.parse_args()
    return opt



def main(opt):
    asyncio.run(run(**vars(opt)))

if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device, opt.poseweights)
    main(opt)

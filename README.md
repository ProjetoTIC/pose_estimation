# Tutorial Detecção de queda idoso

## 1.	Clone o repo o diretório utilizando Terminal
``` git clone  https://github.com/ProjetoTIC/pose_estimation/ ```

Or 

## 2.	Crie um novo ambiente Conda

``` conda env create -f environment.yml ```

Ative o novo ambiente Conda  
``` conda activate yolov7pose ```


## 3.	Navegue até a pasta pose-estimation  
``` cd pose-estimation ```

## 4.	Baixe os Pose Weights e coloque na pasta pose-estimation
https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6-pose.pt 

Ou use no Ubuntu:

``` wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6-pose.pt ```
## 5. Instale as dependencias:

``` pip install -r requirements.txt```

## 6. Rode o codigo no Terminal:

``` python run_pose.py  –-source 0 ```

Para rodar com caminho de video:

``` python run_pose.py  –-source [path to video]```

Para rodar na GPU:

``` python run_pose.py  –-source 0  –-device 0 ```


## Referencias
YOLOv7 - https://github.com/WongKinYiu/yolov7 

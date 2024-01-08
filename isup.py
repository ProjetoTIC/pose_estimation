import cv2

def isUpL(image, kpts, p1, p2, p3, draw=True):
    coord = []
    no_kpts = len(kpts)//3
    for i in range(no_kpts):
        cx, cy = kpts[3*i], kpts[3*i + 1]
        conf = kpts[3*i + 2]
        coord.append([i, cx,cy, conf])

    points = (p1,p2,p3)

    x1,y1 = coord[p1][1:3]
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]
    

    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.circle(image, (int(x1),int(y1)), 10 , (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (int(x2),int(y2)), 10 , (0, 255, 0), cv2.FILLED)
        cv2.circle(image, (int(x3),int(y3)), 10 , (0, 0, 255), cv2.FILLED)
       
        
        if y3 < y1:
            
            return True
      

        

    
def isUpR(image, kpts, p1, p2, p3, draw=True):
    coord = []
    no_kpts = len(kpts)//3
    for i in range(no_kpts):
        cx, cy = kpts[3*i], kpts[3*i + 1]
        conf = kpts[3*i + 2]
        coord.append([i, cx,cy, conf])

    points = (p1,p2,p3)

    x1,y1 = coord[p1][1:3]
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]
    

    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.circle(image, (int(x1),int(y1)), 10 , (255, 255, 0), cv2.FILLED)
        cv2.circle(image, (int(x2),int(y2)), 10 , (0, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x3),int(y3)), 10 , (255, 0, 255), cv2.FILLED)
       
        
        if y3 < y1:
            
            return True
            

def Torso(image, kpts, p1, p2, p3, p4, draw=True):
    coord = []
    no_kpts = len(kpts)//3
    for i in range(no_kpts):
        cx, cy = kpts[3*i], kpts[3*i + 1]
        conf = kpts[3*i + 2]
        coord.append([i, cx,cy, conf])

    points = (p1,p2,p3,p4)

    x1,y1 = coord[p1][1:3]
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]
    x4,y4 = coord[p4][1:3]
    

    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2),int(y2)), (255, 255, 255), 3 )
        cv2.line(image, (int(x3),int(y3)),(int(x4),int(y4)), (255, 255, 255), 3 )
        cv2.line(image, (int(x1),int(y1)),(int(x4),int(y4)), (255, 255, 255), 3 )
        cv2.circle(image, (int(x1),int(y1)), 10 , (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (int(x2),int(y2)), 10 , (255, 255, 0), cv2.FILLED)
        cv2.circle(image, (int(x3),int(y3)), 10 , (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x4),int(y4)), 10 , (255, 255, 255), cv2.FILLED)
       
        
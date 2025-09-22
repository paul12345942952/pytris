import pygame
import random

class fallingPiece:
    def __init__(self, structure, pos, rotation):
        self.structure=structure
        self.pos=pos
        self.rotation=rotation

block_colors=[
    (30,30,30),      # empty
    (0, 255, 255),   # I
    (255, 255, 0),   # O
    (160, 0, 240),   # T
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (0, 0, 255),     # J
    (255, 128, 0),   # L
    (255, 255, 255)  #Full Line
]

blocks=[
    [#I
     [[0,0,1,0], 
      [0,0,1,0],
      [0,0,1,0],
      [0,0,1,0]],

     [[0,0,0,0],
      [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0]],
     
     [[0,0,1,0],
      [0,0,1,0],
      [0,0,1,0],
      [0,0,1,0]],

     [[0,0,0,0],
      [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0]]
    ],
    
    [#O
     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]]
    ],
     
    [#T
     [[0,0,0],
      [3,3,3],
      [0,3,0]],

     [[0,3,0],
      [3,3,0],
      [0,3,0]],

     [[0,3,0],
      [3,3,3],
      [0,0,0]],

     [[0,3,0],
      [0,3,3],
      [0,3,0]]
    ],
    
    [#S
     [[0,0,0],
      [0,4,4],
      [4,4,0]],
    
     [[4,0,0],
      [4,4,0],
      [0,4,0]],
     
     [[0,0,0],
      [0,4,4],
      [4,4,0]],
     
     [[4,0,0],
      [4,4,0],
      [0,4,0]],
    ],
    
    [#Z
     [[0,0,0],
      [5,5,0],
      [0,5,5]], 
       
     [[0,0,5],
      [0,5,5],
      [0,5,0]],
       
     [[0,0,0],
      [5,5,0],
      [0,5,5]],
       
     [[0,0,5],
      [0,5,5],
      [0,5,0]],
    ],
    
    [#J
     [[0,6,0],
      [0,6,0],
      [6,6,0]],
    
     [[0,0,0],
      [6,0,0],
      [6,6,6]], 
    
     [[0,6,6],
      [0,6,0],
      [0,6,0]],
    
     [[0,0,0],
      [6,6,6],
      [0,0,6]],
    ],
    
    [#L
     [[0,7,0],
      [0,7,0],
      [0,7,7]],
     
     [[0,0,0],
      [7,7,7],
      [7,0,0]],
     
     [[7,7,0],
      [0,7,0],
      [0,7,0]],
     
     [[0,0,0],
      [0,0,7],
      [7,7,7]] 
    ]
    ]

blockSize=30
nextPieceReady=True
score=0
#Tetris field = 10*20
#index of block_colors
field=[[0 for x in range(10)] for y in range(20)]

block=random.choice(blocks)[0]
pos=[int((10-len(block[0]))/2),-len(block)]
nextFallingPiece=fallingPiece(block,pos,0)

def drawField():
    rect=pygame.Rect((0,0),(10*blockSize,20*blockSize))
    pygame.draw.rect(surface, (0,0,0), rect)
    for y in range(len(field)):
        for x in range(len(field[0])):
            innerRect=pygame.Rect((x*blockSize+5,y*blockSize+5),(blockSize-10,blockSize-10))
            pygame.draw.rect(surface, block_colors[field[y][x]], innerRect)      
            
def genFallingBlock():
    global currentFallingPiece
    global nextFallingPiece
    global nextPieceReady

    if not nextPieceReady:
        return

    block=random.choice(blocks)[0]
    pos=[int((10-len(block[0]))/2),-len(block)]
    

    currentFallingPiece=nextFallingPiece
    nextFallingPiece=fallingPiece(block,pos,0)

    nextPieceReady=False

def drawFallingBlock(draw):
    structure=currentFallingPiece.structure
    pos=currentFallingPiece.pos
    #drawBlock in field:
    for y in range(pos[1], pos[1]+len(structure)):
        for x in range(pos[0], pos[0]+len(structure[0])):
            if structure[y-pos[1]][x-pos[0]] != 0:
                if draw and y>=0:
                    field[y][x]=structure[y-pos[1]][x-pos[0]] #-startvalue
                elif y>=0:
                    field[y][x]=0

def drawPreview():
    global nextFallingPiece
    structure=nextFallingPiece.structure
    for y in range(4):
        for x in range(4):
            innerRect=pygame.Rect((x*blockSize+5,y*blockSize+5),(blockSize-10,blockSize-10))
            pygame.draw.rect(surfacePreview, (0,0,0), innerRect)

    for y in range(len(nextFallingPiece.structure)):
        for x in range(len(nextFallingPiece.structure[0])):
            innerRect=pygame.Rect((x*blockSize+5,y*blockSize+5),(blockSize-10,blockSize-10))
            if structure[y][x]!=0:
                pygame.draw.rect(surfacePreview, block_colors[structure[y][x]], innerRect)

def handleFallingBlock():
    global nextPieceReady
    if nextPieceReady:
        return
    drawFallingBlock(False)
    lowestY=0
    for y in range(len(currentFallingPiece.structure)):
        for x in range(len(currentFallingPiece.structure[y])):
            if currentFallingPiece.structure[y][x]!=0:
                lowestY=y
    lowestY=currentFallingPiece.pos[1]+lowestY
    move=True

    if lowestY>-2:
        if lowestY>=19:
            move=False
            drawFallingBlock(True)
            checkLine()
            nextPieceReady=True
            return
        else:
            for y in range(len(currentFallingPiece.structure)):
                for x in range(len(currentFallingPiece.structure[0])):
                    if currentFallingPiece.structure[y][x]!=0 and currentFallingPiece.pos[1]+y+1>=0:
                        if field[currentFallingPiece.pos[1]+y+1][currentFallingPiece.pos[0]+x]!=0:
                            move=False
                            drawFallingBlock(True)
                            checkLine()
                            nextPieceReady=True
                            return
    if move:
        currentFallingPiece.pos[1]+=1
    drawFallingBlock(True)

def moveFallingBlock(dir):
    global currentFallingPiece
    drawFallingBlock(False)
    offset= 1 if dir=="right" else -1
    move=True

    minX=100 #erster Block (1) in X
    maxX=-1 #letzter Block in X

    for y in currentFallingPiece.structure:
        for x in range(len(y)):
            if y[x]!=0:
                if x<minX:
                    minX=x
                elif x>maxX:
                    maxX=x

    if (currentFallingPiece.pos[0]+minX<=0 and dir=="left") or (currentFallingPiece.pos[0]+maxX>=9 and dir=="right"):
        move=False
    else:
        for y in range(len(currentFallingPiece.structure)):
            for x in range(len(currentFallingPiece.structure[0])):
                try:
                    if currentFallingPiece.structure[y][x]!=0: #Luft neben block
                        if field[currentFallingPiece.pos[1]+y][currentFallingPiece.pos[0]+x+offset]!=0:
                            move=False
                except: #auch Luft neben Block da oben Error
                    try:
                        if field[currentFallingPiece.pos[1]+y][currentFallingPiece.pos[0]+x+offset]!=0:
                            move=False
                    except: #Block ganz unten deswegen y index out of range
                        move=False

    if move:
        currentFallingPiece.pos[0]+=offset
    drawFallingBlock(True)

def rotate():
    global currentFallingPiece
    rotate=True
    drawFallingBlock(False)
    blockNum=-1
    for y in currentFallingPiece.structure:
        for x in y:
            if x !=0:
                blockNum=x-1

    #check rotation
    pos=currentFallingPiece.pos
    rotatedStructure=blocks[blockNum][(currentFallingPiece.rotation+1)%4]
    
    minX=100 #erster Block (1) in X
    maxX=-1 #letzter Block in X

    for y in rotatedStructure:
        for x in range(len(y)):
            if y[x]!=0:
                if x<minX:
                    minX=x
                elif x>maxX:
                    maxX=x

    if currentFallingPiece.pos[0]+minX<0 or currentFallingPiece.pos[0]+maxX>9:
        rotate=False
    else:
        for y in range(len(rotatedStructure)):
            for x in range(len(rotatedStructure[0])):
                if rotatedStructure[y][x]!=0 and field[pos[1]+y][pos[0]+x]!=0: #Block in structure und Block im Field überlappen sich
                    rotate=False

    if rotate:
        currentFallingPiece.structure=rotatedStructure
        currentFallingPiece.rotation+=1
    drawFallingBlock(True)

def checkLine():
    global field
    global score
    newField=[]
    linesCleared=0
    for y in range(len(field)):
        if 0 not in field[y]:
            linesCleared+=1
            score+=1
            highLightLine(y)
        else:
            newField.append(field[y])
    highlight_delay = 1000  # milliseconds
    last_time = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        if now-last_time>=highlight_delay:
            break
    
    for _ in range(linesCleared):
        newField.insert(0, [0 for x in range(10)])
    
    drawScore()
    field=newField

def highLightLine(y):
    rect=pygame.Rect((0,y*blockSize),(blockSize*10,blockSize))
    pygame.draw.rect(surface, (255,255,255), rect)
    screen.blit(surface,(0,0))
    pygame.display.update()

def drawScore():
    global score
    global text_surface
    pygame.draw.rect(screen, (0, 0, 0), (330, 200, 100, 40))
    text_surface = my_font.render(f'{score}', False, (255, 255, 255))
    screen.blit(text_surface, (0,0))

def checkGameOver():
    global gameOver
    if (field[0][3] !=0 or field[0][4] !=0 or field[0][4]!=0 or field[0][4] !=0) and nextPieceReady:
        gameOver=True

def reset():
    global score
    global field
    global currentFallingPiece
    global nextPieceReady
    score=0
    field=[[0 for x in range(10)] for y in range(20)]
    currentFallingPiece=None
    nextPieceReady=True
    drawScore()


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen=pygame.display.set_mode((500,600))
surface=pygame.Surface((blockSize*10,blockSize*20))
surfacePreview=pygame.Surface((blockSize*4,blockSize*4))
text_surface = my_font.render('0', False, (255, 255, 255))
pygame.display.set_caption("PyTris")


running=True
gameOver=False
move_delay = 1000  # milliseconds
last_move_time = pygame.time.get_ticks()

move_delay_down=100
last_move_time_down = pygame.time.get_ticks()

move_delay_side=200
last_move_time_side = pygame.time.get_ticks()

while running:
    while not gameOver:
        move_delay=1000-score*10 if 1000-score*10 >=100 else 100
        drawField()
        genFallingBlock()
        drawPreview()
        now=pygame.time.get_ticks()
        if now-last_move_time>=move_delay: 
            handleFallingBlock()
            checkGameOver()
            last_move_time=now
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    running=False
                if event.key==pygame.K_SPACE or event.key==pygame.K_UP or event.key==pygame.K_w:
                    rotate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if now-last_move_time_side>=move_delay_side:
                moveFallingBlock("left")
                last_move_time_side=now
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if now-last_move_time_side>=move_delay_side:
                moveFallingBlock("right")
                last_move_time_side=now
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if now-last_move_time_down>=move_delay_down:
                handleFallingBlock()
                last_move_time_down=now
        if keys[pygame.K_r]:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 500, 600))
            gameOver=False
            reset()
            

        screen.blit(surface,(0,0))
        screen.blit(surfacePreview,(330,0))
        screen.blit(text_surface,(330,200))
        pygame.display.update()

        if not running: 
            break
    while gameOver:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 500, 600))
        text_surface = my_font.render('GAME OVER, R TO TRY AGAIN', False, (255, 0, 0))
        screen.blit(text_surface, (25,220))

        for event in pygame.event.get():
            if event.type==pygame.QUIT or event.type==pygame.K_q:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                        running=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_r]:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 500, 600))
            gameOver=False
            reset()
        pygame.display.update()

        if not running: 
            break
pygame.quit()
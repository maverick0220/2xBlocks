from __future__ import annotations  # 因为ChessBlock类需要在未完成定义前引用自己，所以用了这个语法糖
import data

class ChessBlock:
    def __init__(self, y, x, initValue: data.Data):
        self.y = y
        self.x = x

        self.value = initValue.value  # -1表示这是个空的block
        self.index = initValue.index  # 代表在dataIndex里面的索引，因为最多才五百多个，所以这个值的invalid数值定成-1，肯定会超过索引范围
        self.color = initValue.color

        self.isCenter = False

        # -todo： 还没理清楚，这个东西要clear状态在什么地方clear
        self.mergeVector = -1  # 1, 2, 3, 4，上右下左顺时针，标识这个block如果要发生聚合的话是往哪个方向聚合

    def update(self, value: data.Data | ChessBlock):
        if isinstance(value, ChessBlock):
            self.isCenter = value.isCenter
        self.value = value.value
        self.index = value.index
        self.color = value.color

    def isSameWithBlock(self, block) -> bool:
        if block.value == self.value and block.index == self.index:
            return True
        return False

class Chessboard:
    def __init__(self):

        self.dataProcess = data.DataProcess()

        # load save
        gameSave = [line.strip().split(",") for line in open("./gameSave.csv", "r")]

        self.size_y = len(gameSave)  # 7行，每行5列
        self.size_x = len(gameSave[0])

        # 注意：board最后有一行是隐形的，如果到顶了，相同的色块照样往下合并，不同的就直接gg
        self.board = [[ChessBlock(y, x, self.dataProcess.translateStrToData(gameSave[y][x])) for x in range(self.size_x)] for y in range(self.size_y)]
        self.board.append([ChessBlock(self.size_y, x, data.Data("", -1)) for x in range(self.size_x)])

        # - todo: 这里应该是持续地生成nextBlockQueue的内容，现在只是放进去了测试的内容
        self.dataRange = self.dataProcess.getDataRange(self.board)
        self.nextBlockQueue = [] #[ChessBlock(0, 2, data.Data("1024", 11)) for i in range(2)]  # self.createNextBlock
        self.refreshNextBlockQueue()

        self.slot = [ChessBlock(0, i, data.Data("", -1)) for i in range(5)]
        self.slot[2] = self.nextBlockQueue[0]
        self.nextBlockSlotIndex = 2

        self.canGamerOperate = True

    def refreshNextBlockQueue(self):
        # 创建新的block塞到self.nextBlockQueue最后，然后把最前面的踢掉
        if len(self.nextBlockQueue) == 2:
            del self.nextBlockQueue[0]

        for i in range(2 - len(self.nextBlockQueue)):
            self.nextBlockQueue.append(ChessBlock(0, -1, self.dataProcess.getRandomDataFromRange(self.dataRange)))

    def printBoard(self):
        for line in self.board:
            print([b.value for b in line])
        print(" ")
        for line in self.board:
            row = []
            for b in line:
                if b.isCenter:
                    row.append("Y")
                else:
                    row.append("N")
            print(row)
        print("==============")

    def sendBlock(self) -> bool:
        didSend = False
        for y in range(self.size_y):
            if self.board[y][self.nextBlockSlotIndex].value == "":
                self.board[y][self.nextBlockSlotIndex].update(self.slot[self.nextBlockSlotIndex])
                self.board[y][self.nextBlockSlotIndex].isCenter = True
                didSend = True
                break

        self.slot[self.nextBlockSlotIndex] = ChessBlock(0, self.nextBlockSlotIndex, data.Data("", -1))

        self.refreshNextBlockQueue()
        self.slot[self.nextBlockSlotIndex] = self.nextBlockQueue[0]

        return didSend

    def moveSlot(self, key: str):
        # self.canGamerOperate = False
        if key == "a" or key == "arrow left":
            self.slot = self.slot[1:] + [self.slot[0]]
            if self.nextBlockSlotIndex == 0:
                self.nextBlockSlotIndex = self.size_x - 1
            else:
                self.nextBlockSlotIndex -= 1
        elif key == "d" or key == "arrow right":
            self.slot = [self.slot[-1]] + self.slot[:-1]
            self.nextBlockSlotIndex = (self.nextBlockSlotIndex + 1) % self.size_x
        # self.canGamerOperate = True

    def _erasureBlocks(self, blocks: list[ChessBlock]):
        for b in blocks:
            self.board[b.y][b.x].value = ""
            self.board[b.y][b.x].index = -1
            self.board[b.y][b.x].color = "#B5B5B5"
            self.board[b.y][b.x].mergeVector = -1
            self.board[b.y][b.x].isCenter = False
        # self.updateView()

    def _erasureMergedBlocks(self, mergeCenter: ChessBlock, blocks: list[ChessBlock]):
        '''这个方法和_erasureBlocks的区别在于，会更新mergeVector然后擦除其他的信息'''

        def getRelativeDirection(s: [int], e: [int]) -> int:
            if s[0] == e[0]:
                if s[1] == e[1] - 1:
                    return 3
                elif s[1] == e[0] + 1:
                    return 1
            elif s[1] == e[1] and s[0] == e[0] + 1:
                return 2
            return -1

        for b in blocks:
            self.board[b.y][b.x].value = ""
            self.board[b.y][b.x].index = -1
            self.board[b.y][b.x].color = "#B5B5B5"

            self.board[b.y][b.x].mergeVector = getRelativeDirection([b.y, b.x], [mergeCenter.y, mergeCenter.x])

    def _getNearbyCompateableBlocks(self, center: ChessBlock) -> list[ChessBlock]:
        '''
        把中心block周围相同值的block都给找出来
        '''
        nearbyCompateableBlock = []

        if 0 < center.x and center.isSameWithBlock(self.board[center.y][center.x - 1]):
            nearbyCompateableBlock.append(self.board[center.y][center.x - 1])
        if center.x < self.size_x - 1 and center.isSameWithBlock(self.board[center.y][center.x + 1]):
            nearbyCompateableBlock.append(self.board[center.y][center.x + 1])
        if 0 < center.y and center.isSameWithBlock(self.board[center.y - 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y - 1][center.x])
        if center.y < self.size_y - 1 and center.isSameWithBlock(self.board[center.y + 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y + 1][center.x])

        return nearbyCompateableBlock
    
    def checkChessboard(self) -> data.Event:
        # merge & fall，这必须是一个自递归的方法，因为每一步的操作都得反馈给UI那边做渲染，不然就是丢一个方块看不到过程只能看到结果
        # 因为是自递归的，不要想着一次性干完所有事情，而是只干一次，剩下的下次再干。每次干的结果都要反馈给UI那边
        # 要反馈的东西有两类，发生了聚合、发生了下坠
        
        # 只有新聚合出现的block才被标记为newCenter。
        # 检查有没有newCenter，有就聚合并把新聚合出来的标记成newCenter并擦除被聚合的
        # checkResultEvent = data.Event("", [])

        # 1.先找找有没有fall的
        columnDidFall = [0 for _ in range(self.size_x)]
        for x in range(self.size_x):
            # 先看看有没有空，确定到底有没有fall
            columnInfo = [1 if self.board[y][x].value != "" else 0 for y in range(self.size_y)]
            # print(f"== checkChessboard fall column len1: {len(columnInfo)}")
            while columnInfo and columnInfo[-1] == 0:
                columnInfo.pop()
            # print(f"== checkChessboard fall column len2: {len(columnInfo)}, {sum(columnInfo)}\n")
            if len(columnInfo) > sum(columnInfo):
                # 执行fall
                columnDidFall[x] = 1

                columnData = [self.board[y][x] for y in range(self.size_y) if self.board[y][x].value != ""]
                for y in range(0, len(columnData)):
                    self.board[y][x].update(columnData[y])
                    if columnData[y].y != y:  # 有位移的才更新isCenter
                        self.board[y][x].isCenter = True
                self._erasureBlocks([self.board[y][x] for y in range(len(columnData), self.size_y)])
            else:
                # 没有需要fall的，pass，看下一列吧
                continue
            
        if sum(columnDidFall) > 0:
            print("== checkChessboard: did fall")
            return data.Event("fall", [])

        # 2.再找找有没有聚合的
        newCenterBlocks = []
        self.printBoard()
        for y in range(self.size_y):
            for x in range(self.size_x):
                # print(f"== newCenterBlocks: {y},{x} {self.board[y][x].isCenter}")
                if self.board[y][x].isCenter:
                    newCenterBlocks.append(self.board[y][x])
        # print(f"== newCenterBlocks: {newCenterBlocks}")
        if newCenterBlocks == None:
            return data.Event("", [])
        
        didNewCenterBlockMerged = []
        toMergeBlocks = []  # - todo: 这个是需要传回给前端的东西，告诉前端哪些block需要有聚合的动画
        for ncBlock in newCenterBlocks:
            nearbyCompateables = self._getNearbyCompateableBlocks(ncBlock)
            # print(f"checkChessboard: ({ncBlock.y}, {ncBlock.x}) nearbyCompateables: {len(nearbyCompateables)}")
            if len(nearbyCompateables) > 0:
                didNewCenterBlockMerged.append(1)
                mergedBlock = self.mergeBlocks(ncBlock, nearbyCompateables)
                self.board[ncBlock.y][ncBlock.x].update(mergedBlock)
                self.board[ncBlock.y][ncBlock.x].isCenter = True
                self._erasureMergedBlocks(ncBlock, nearbyCompateables)
                ncBlock.isCenter = True

                toMergeBlocks.append([ncBlock] + nearbyCompateables)
            else:
                didNewCenterBlockMerged.append(0)
                ncBlock.isCenter = False
            
        if sum(didNewCenterBlockMerged) == 0:
            return data.Event("", [])
        # print("== checkChessboard: did merge")
        return data.Event("merge", toMergeBlocks)

    def mergeBlocks(self, center: ChessBlock, blocks: list[ChessBlock]) -> ChessBlock:
        upgradeIndex = center.index + 1 * len(blocks)
        mergedValue = self.dataProcess.dataIndex[upgradeIndex]  #(2 ** (len(blocks))) * center.value
        print(f"mergeBlocks value: {center.value}, {len(blocks)}, {mergedValue}")
        mergedData = data.Data(mergedValue, upgradeIndex)
        # if mergedValue > 10000:
        #     mergedData.value = mergedData.value / 10000
        #     mergedData.upgradeRank()

        mergedBlock = ChessBlock(center.y, center.x, mergedData)
        mergedBlock.isCenter = True

        return mergedBlock

    def saveGameToFile(self):
        pass
import flet as ft
import time
from chessboard import *

def main(page: ft.Page):
    chessboard = Chessboard()

    # 页面设置
    page.title = "7×5 圆角矩形阵列"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中
    page.vertical_alignment = ft.MainAxisAlignment.START      # 垂直居中
    spacing = 4

    def update_allView():
        update_chessboardView()
        update_slotView()

    def update_chessboardView():
        """当chessboard.board数据变化时，同步更新控件显示"""
        for y in range(chessboard.size_y):
            for x in range(chessboard.size_x):
                chessboard_controls[y][x].bgcolor = chessboard.board[y][x].color
                chessboard_controls[y][x].content.value = chessboard.board[y][x].getText()
        page.update()

    def update_slotView():
        """当chessboard.slot数据变化时，同步更新控件显示"""
        for i in range(len(slot_controls)):
            slot_controls[i].bgcolor = chessboard.slot[i].color
            slot_controls[i].content.value = chessboard.slot[i].getText()
        page.update()


    #  ========
    def merge_example(center_pos: [int], target_positions: [[int]]):
        """
        合并动画核心函数
        :param center_pos: 中心块位置 [y, x]，作为吸引源
        :param target_positions: 被吸引的块位置列表，如 [[y1, x1], [y2, x2]]
        """
        print(target_positions)
        # 解析中心块坐标和控件
        ci, cj = center_pos
        center_block = chessboard_controls[ci][cj]
        if not center_block:
            print("中心块不存在")
            return

        # 验证所有目标块是否与中心块相邻
        valid_targets = []
        for tp in target_positions:
            # 检查是否在棋盘范围内
            print(tp[1])
            if 0 <= tp[0] < len(chessboard_controls) and 0 <= tp[1] < len(chessboard_controls[0]):
                # 检查是否与中心块相邻（水平或垂直）
                if (tp[0] == ci and abs(tp[1] - cj) == 1) or (tp[1] == cj and abs(tp[1] - ci) == 1):
                    valid_targets.append((tp[0], tp[1]))
                else:
                    print(f"({tp[0]},{tp[1]}) 与中心块不相邻，跳过")
            else:
                print(f"({tp[0]},{tp[1]}) 超出棋盘范围，跳过")

        if not valid_targets:
            print("无有效合并目标")
            return

        # 存储原始属性（用于动画结束后重置，可选）
        original_props = []
        for (ti, tj) in valid_targets:
            target = chessboard_controls[ti][tj]
            original_props.append({
                "target": target,
                "width": target.width,
                "height": target.height,
                "left": target.left,
                "top": target.top,
                "opacity": target.opacity,
                "visible": target.visible
            })

        # 计算动画参数并启动动画
        def animate_step():
            for (ti, tj) in valid_targets:
                target = chessboard_controls[ti][tj]
                # 判断相邻方向（水平/垂直）
                if ti == ci:  # 水平相邻（同一行）
                    # 目标块在中心块左侧（tj < cj）
                    if tj < cj:
                        # 拉长效果：宽度增加（向中心方向延伸），高度保持不变
                        target.width = 60 + (cj - tj) * (60 + spacing)  # 覆盖到中心块的距离
                        target.left = -(cj - tj) * (60 + spacing)  # 向左移动，靠近中心
                    # 目标块在中心块右侧（tj > cj）
                    else:
                        target.width = 60 + (tj - cj) * (60 + spacing)
                        target.left = 0  # 向右延伸覆盖中心块

                else:  # 垂直相邻（同一列）
                    # 目标块在中心块上方（ti < ci）
                    if ti < ci:
                        # 拉长效果：高度增加，宽度保持不变
                        target.height = 60 + (ci - ti) * (60 + spacing)
                        target.top = -(ci - ti) * (60 + spacing)  # 向上移动靠近中心
                    # 目标块在中心块下方（ti > ci）
                    else:
                        target.height = 60 + (ti - ci) * (60 + spacing)
                        target.top = 0  # 向下延伸覆盖中心块

                # 逐渐透明（消失效果）
                target.opacity = 0.3
                # 保持可见直到动画结束
                target.visible = True

            # 刷新页面触发第一阶段动画（拉长+移动）
            page.update()

            # 延迟后执行第二阶段（完全消失+中心块更新）
            page.run_task(lambda: complete_merge(valid_targets, center_block))

        # 动画完成后处理
        def complete_merge(targets, center):
            # 隐藏所有被合并的块
            for (ti, tj) in targets:
                chessboard_controls[ti][tj].visible = False

            # 更新中心块文本（示例：合并后的文本）
            # 实际业务中可从chessboard获取合并后的值
            current_text = center.content.value
            center.content.value = f"合并{current_text}"  # 示例：拼接文本
            center.bgcolor = ft.colors.with_opacity(0.9, center.bgcolor)  # 可选：强化中心块视觉

            # 刷新最终状态
            page.update()

        # 启动动画
        animate_step()

    # 为了演示合并，添加一个测试按钮（实际场景中可替换为你的判断逻辑）
    test_merge_btn = ft.ElevatedButton(text="合并(0,0)和(0,1)",
                                       on_click=lambda e: merge_example((2,2), [(2,1), (2,3)]))
    page.add(test_merge_btn)
    #  ========


    # 监听摁键
    def on_keyboard(e: ft.KeyboardEvent):
        if chessboard.canGamerOperate == False:
            return

        if e.key in ["A", "a", "D", "d", "ArrowRight", "Arrow Right", "ArrowLeft", "Arrow Left"]:
            chessboard.moveSlot(e.key.lower())
            update_slotView()
        if e.key in ["W", "w", "ArrowUp", "Arrow Up"]:
            chessboard.printBoard()
            if chessboard.sendBlock():
                update_allView()
                time.sleep(0.4)
                temp_count = 0
                while(temp_count < 3):
                    # if temp_count > 3:
                    #     break
                    chessboard.printBoard()
                    
                    checkResult = chessboard.checkChessboard()  # 在checkChessboard里面就已经聚合过后台了
                    update_allView()
                    # temp_count += 1
                    time.sleep(0.4)
                    if checkResult.isValidEvent:
                        continue
                    elif len(checkResult.relativeBlockGroups) == 0:
                        break

                    
                # -todo: 更新聚合后模型的UI。到这个时候后台该干的事儿都干完了

                # chessboard.printBoard()
            update_allView()

    # 绑定键盘事件
    page.on_keyboard_event = on_keyboard

    # 1.chessboardView
    chessboardView = ft.Column(spacing=spacing, controls=[])
    chessboard_controls = []
    for y in range(chessboard.size_y):
        row = ft.Row(spacing=spacing, controls=[])
        control_row = []

        for block in chessboard.board[y]:
            rect = ft.Container(width=60, height=60, bgcolor=block.color, border_radius=10, alignment=ft.alignment.center,
                                content=ft.Text(value=block.getText(), color="black", weight=ft.FontWeight.BOLD))
            control_row.append(rect)
            row.controls.append(rect)  # 添加到当前行
        chessboardView.controls.append(row)  # 将行添加到网格
        chessboard_controls.append(control_row)
    page.add(chessboardView)

    # 2.slotView
    slotRow = ft.Row(spacing=spacing, controls=[])
    slot_controls = []

    for block in chessboard.slot:
        rect = ft.Container(width=60, height=60, bgcolor=block.color, border_radius=10, alignment=ft.alignment.center,
                            content=ft.Text(value=block.getText(), color="black", weight=ft.FontWeight.BOLD))
        slot_controls.append(rect)
        slotRow.controls.append(rect)
    page.add(slotRow)
    page.update()

# 启动应用
ft.app(target=main)
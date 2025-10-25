import flet as ft
from chessboard import *
import time


def main(page: ft.Page):
    chessboard = Chessboard()

    # 页面设置
    page.title = "7×5 圆角矩形阵列"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平居中
    page.vertical_alignment = ft.MainAxisAlignment.START  # 垂直居中
    spacing = 4

    def update_allView():
        update_chessboardView()
        update_slotView()

    def update_chessboardView():
        """当chessboard.board数据变化时，同步更新控件显示"""
        for i in range(chessboard.size_y):
            for j in range(chessboard.size_x):
                chessboard_controls[i][j].bgcolor = chessboard.board[i][j].color
                chessboard_controls[i][j].content.value = chessboard.board[i][j].getText()
        page.update()

    def update_slotView():
        """当chessboard.slot数据变化时，同步更新控件显示"""
        for i in range(len(slot_controls)):
            slot_controls[i].bgcolor = chessboard.slot[i].color
            slot_controls[i].content.value = chessboard.slot[i].getText()
        page.update()

    def merge_example(center_pos: [int], target_positions: [[int]]):
        """
        合并动画核心函数
        :param center_pos: 中心块位置 [y, x]，作为吸引源
        :param target_positions: 被吸引的块位置列表，如 [[y1, x1], [y2, x2]]
        """
        center_y, center_x = center_pos

        # 获取中心方块的控件
        center_control = chessboard_controls[center_y][center_x]

        # 获取目标方块的控件
        target_controls = []
        for y, x in target_positions:
            target_controls.append(chessboard_controls[y][x])

        # 记录原始样式
        original_styles = []
        for control in target_controls:
            original_styles.append({
                'scale': control.scale or 1.0,
                'opacity': control.opacity or 1.0
            })

        # 动画过程 - 分15步进行
        total_steps = 15
        for step in range(total_steps):
            progress = step / (total_steps - 1)  # 从0到1

            # 计算变形和移动效果
            for i, target_control in enumerate(target_controls):
                # 缩放效果 - 模拟被拉伸变形
                scale_x = max(0.3, 1.0 - progress * 0.7)  # 宽度缩小
                scale_y = max(0.1, 1.0 - progress * 0.9)  # 高度大幅缩小，模拟拉长效果

                # 透明度变化
                opacity = max(0.1, 1.0 - progress * 0.95)

                # 应用变换
                target_control.scale = ft.Animation(scale_x, scale_y)
                target_control.opacity = opacity

            page.update()
            time.sleep(0.005)  # 动画延迟，使动画更流畅

        # 动画完成后，执行实际的合并逻辑
        # chessboard.merge_blocks(center_pos, target_positions)

        # 更新视图显示
        update_allView()

        # 重置样式
        for i, target_control in enumerate(target_controls):
            target_control.scale = original_styles[i]['scale']
            target_control.opacity = original_styles[i]['opacity']

    # 为了演示合并，添加一个测试按钮（实际场景中可替换为你的判断逻辑）
    test_merge_btn = ft.ElevatedButton(text="合并示例",
                                       on_click=lambda e: merge_example((2, 2), [(2, 1), (2, 3)]))
    page.add(test_merge_btn)

    # ========

    # 监听摁键
    def on_keyboard(e: ft.KeyboardEvent):
        if chessboard.canGamerOperate == False:
            return

        if e.key in ["A", "a", "D", "d"]:
            chessboard.moveSlot(e.key.upper())
            update_slotView()
        if e.key in ["W", "w"]:
            chessboard.sendBlock()

            while (True):
                toMergeBlocks = chessboard.checkChessboard()
                if len(toMergeBlocks) == 0:
                    break

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
            rect = ft.Container(
                width=60,
                height=60,
                bgcolor=block.color,
                border_radius=10,
                alignment=ft.alignment.center,
                content=ft.Text(value=block.getText(), color="black", weight=ft.FontWeight.BOLD)
            )
            control_row.append(rect)
            row.controls.append(rect)  # 添加到当前行
        chessboardView.controls.append(row)  # 将行添加到网格
        chessboard_controls.append(control_row)

    # 将网格添加到页面并刷新
    page.add(chessboardView)

    # 2.slotView
    slotRow = ft.Row(spacing=spacing, controls=[])
    slot_controls = []
    for block in chessboard.slot:
        rect = ft.Container(
            width=60,
            height=60,
            bgcolor=block.color,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Text(value=block.getText(), color="black", weight=ft.FontWeight.BOLD)
        )
        slot_controls.append(rect)
        slotRow.controls.append(rect)

    page.add(slotRow)
    page.update()


# 启动应用
ft.app(target=main)
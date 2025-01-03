import pygame
import random
import sys

#初始化
pygame.init()

#设置颜色
WHITE = (255, 255, 255)    #白
BLACK = (0, 0, 0)     #黑
GRAY = (128, 128, 128)   #灰
RED = (255, 0, 0)    #红
GREEN = (0, 255, 0)   #绿
BLUE = (0, 0, 255)     #蓝
LIGHT_BLUE = (173, 216, 230) #浅蓝
BEIGE = (245, 245, 220)  #米色
MINT_GREEN = (152, 255, 152)   #薄荷绿
LAVENDER = (230, 230, 250)  #薰衣草
LIGHT_SLATE_GRAY = (119, 136, 153)  #浅灰蓝
LIGHT_CORAL = (240, 128, 128)   #浅珊瑚
GOLDEN = (255, 215, 0)   # 金色

#设置屏幕大小
size = (500,600)
screen = pygame.display.set_mode(size)
#设置标题
pygame.display.set_caption('2048')
#设置字体
font = pygame.font.SysFont('HeiTi', 100)
small_font = pygame.font.SysFont('SimHei', 40)
solo_font = pygame.font.SysFont('SimHei', 65)
re_font = pygame.font.SysFont('SimHei', 24)
# 加载图标图像
icon_image = pygame.image.load('图标.png')  # 替换为你的图片路径
pygame.display.set_icon(icon_image)

# 绘制圆角矩形
def draw_rounded_rect(surface, color, rect, radius=4):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + rect[3] - radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + rect[3] - radius), radius)
    pygame.draw.line(surface, color, (rect[0] + radius, rect[1]), (rect[0] + rect[2] - radius, rect[1]), 5)
    pygame.draw.line(surface, color, (rect[0], rect[1] + radius), (rect[0], rect[1] + rect[3] - radius), 5)
    pygame.draw.line(surface, color, (rect[0] + rect[2], rect[1] + radius), (rect[0] + rect[2], rect[1] + rect[3] - radius), 5)
    pygame.draw.line(surface, color, (rect[0] + radius, rect[1] + rect[3]), (rect[0] + rect[2] - radius, rect[1] + rect[3]), 5)

# 主菜单界面
def show_menu():
    in_menu = True
    while in_menu:
        screen.fill(BEIGE)

        # 标题
        title_text = font.render("2048", True, GOLDEN)
        screen.blit(title_text, (170, 100))

        # 模式选择按键
        buttons = [
            ("4x4", (125, 245), (250, 50)),
            ("5x5", (125, 345), (250, 50)),
            ("障碍模式", (125, 445), (250, 50)),
        ]
        for text, pos, size in buttons:
            draw_rounded_rect(screen, GOLDEN, (pos[0], pos[1], size[0], size[1]))
            button_text = small_font.render(text, True, BLACK)
            screen.blit(button_text, (pos[0] + (size[0] - button_text.get_width()) // 2,
                                      pos[1] + (size[1] - button_text.get_height()) // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for text, pos, size in buttons:
                    if pos[0] < x < pos[0] + size[0] and pos[1] < y < pos[1] + size[1]:
                        return text

#存储全局数据的结构
class GameData:
    def __init__(self, size, obstacles=False):
        self.size = size
        self.obstacles = obstacles
        self.data = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0

# 绘制返回按钮
def draw_back_button():
    #pygame.draw.rect(screen, LIGHT_SLATE_GRAY, (10, 10, 70, 30))
    # 定义箭头形状
    arrow_points = [
        (15, 25),  # 箭头尾部
        (35, 15),  # 箭头上角
        (35, 20),  # 箭头右上角
        (55, 20),  # 箭头右顶
        (55, 30),  # 箭头右下角
        (35, 30),  # 箭头底部
        (35, 35),  # 箭头尾部对称点
    ]
    # 使用白色填充箭头形状
    pygame.draw.polygon(screen, WHITE, arrow_points)
#数字颜色
def get_color_for_value(value):
    colors = {
        2: (238, 228, 218),     # 浅米色
        4: (237, 224, 200),     # 浅橙色
        8: (242, 177, 121),     # 橙色
        16: (245, 149, 99),     # 深橙色
        32: (246, 124, 95),     # 红色
        64: (246, 94, 59),      # 深红色
        128: (237, 207, 114),   # 金色
        256: (237, 204, 97),    # 深金色
        512: (237, 200, 80),    # 更深金橙色
        1024: (237, 197, 63),   # 深金黄色
        2048: (237, 194, 46),   # 黄金色
    }
    # 默认颜色
    return colors.get(value, (205, 193, 180))  # 用于未知或大于2048的值

#游戏初始化
def init_game(game_data):
    game_data.data = [[0 for _ in range(game_data.size)] for _ in range(game_data.size)]
    game_data.score = 0

    # 生成随机障碍块 (-1: 障碍)
    if game_data.obstacles:
        obstacle_count = random.randint(1, 2)  # 随机生成2到4个障碍块
        while obstacle_count > 0:
            row = random.randint(0, game_data.size - 1)
            col = random.randint(0, game_data.size - 1)
            if game_data.data[row][col] == 0:
                game_data.data[row][col] = -1
                obstacle_count -= 1
    # 随机生成两个初始数字
    for _ in range(2):
        placed = False
        while not placed:
            row = random.randint(0, game_data.size - 1)
            col = random.randint(0, game_data.size - 1)
            if game_data.data[row][col] == 0:
                game_data.data[row][col] = random.choice([2, 4])
                placed = True


#游戏绘制
def draw_game(game_data):
    screen.fill(GRAY)   #背景颜色
    #得分区
    score_text = small_font.render(f"Score: {game_data.score}", True, WHITE)
    screen.blit(score_text, (10, 40))
    #网格大小设置
    grid_size = game_data.size
    cell_size = 500 // grid_size
    # 绘制网格
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size + 100
            background_color = WHITE
            if game_data.data[row][col] == -1:
                background_color = RED  # 障碍块颜色
            else:
                background_color = get_color_for_value(game_data.data[row][col])
            pygame.draw.rect(screen, background_color, [x, y, cell_size, cell_size])
            pygame.draw.rect(screen, WHITE, [x, y, cell_size, cell_size], 1)
            if game_data.data[row][col] > 0:  # 绘制数字
                num_text = small_font.render(str(game_data.data[row][col]), True, BLACK)
                text_rect = num_text.get_rect()
                text_rect.centerx = x + cell_size // 2
                text_rect.centery = y + cell_size // 2
                screen.blit(num_text, text_rect)
#上
def move_up(game_data):
    size = game_data.size
    data = game_data.data
    score = game_data.score
    moved = False  # 用于判断是否发生过有效移动或合并
    for col in range(size):
        merged = [False] * size
        for row in range(1, size):
            if data[row][col] > 0:  # 确保是数字块
                target_row = row
                while (target_row > 0 and data[target_row - 1][col] in [0, data[row][col]] and
                       not data[target_row - 1][col] == -1):
                    target_row -= 1
                    moved = True
                if target_row != row:
                    if data[target_row][col] == data[row][col] and not merged[target_row]:
                        data[target_row][col] *= 2
                        score += data[target_row][col]
                        data[row][col] = 0
                        merged[target_row] = True
                    else:
                        if data[target_row][col] == 0:
                            data[target_row][col] = data[row][col]
                            data[row][col] = 0
    game_data.score = score
    return moved
#下
def move_down(game_data):
    size = game_data.size
    data = game_data.data
    score = game_data.score

    moved = False

    for col in range(size):
        merged = [False] * size
        for row in range(size - 2, -1, -1):
            if data[row][col] > 0:
                target_row = row
                while target_row < size - 1 and data[target_row + 1][col] in [0, data[row][col]] and not data[target_row + 1][col] == -1:
                    target_row += 1
                    moved = True
                if target_row != row:
                    if data[target_row][col] == data[row][col] and not merged[target_row]:
                        data[target_row][col] *= 2
                        score += data[target_row][col]
                        data[row][col] = 0
                        merged[target_row] = True
                    else:
                        if data[target_row][col] == 0:
                            data[target_row][col] = data[row][col]
                            data[row][col] = 0
    game_data.score = score
    return moved

# 左
def move_left(game_data):
    size = game_data.size
    data = game_data.data
    score = game_data.score

    moved = False

    for row in range(size):
        merged = [False] * size
        for col in range(1, size):
            if data[row][col] > 0:
                target_col = col
                while target_col > 0 and data[row][target_col - 1] in [0, data[row][col]] and not data[row][target_col - 1] == -1:
                    target_col -= 1
                    moved = True
                if target_col != col:
                    if data[row][target_col] == data[row][col] and not merged[target_col]:
                        data[row][target_col] *= 2
                        score += data[row][target_col]
                        data[row][col] = 0
                        merged[target_col] = True
                    else:
                        if data[row][target_col] == 0:
                            data[row][target_col] = data[row][col]
                            data[row][col] = 0
    game_data.score = score
    return moved

# 右
def move_right(game_data):
    size = game_data.size
    data = game_data.data
    score = game_data.score

    moved = False

    for row in range(size):
        merged = [False] * size
        for col in range(size - 2, -1, -1):
            if data[row][col] > 0:
                target_col = col
                while target_col < size - 1 and data[row][target_col + 1] in [0, data[row][col]] and not data[row][target_col + 1] == -1:
                    target_col += 1
                    moved = True
                if target_col != col:
                    if data[row][target_col] == data[row][col] and not merged[target_col]:
                        data[row][target_col] *= 2
                        score += data[row][target_col]
                        data[row][col] = 0
                        merged[target_col] = True
                    else:
                        if data[row][target_col] == 0:
                            data[row][target_col] = data[row][col]
                            data[row][col] = 0
    game_data.score = score
    return moved

#生成新的数
def generate_new_num(game_data):
    size = game_data.size
    data = game_data.data

    while True:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)

        if data[row][col] == 0:
            data[row][col] = random.choice([2, 4])
            break
    return game_data

#游戏结束
def is_game_over(game_data):
    size = game_data.size
    data = game_data.data
    for row in range(size):
        for col in range(size):
            # 如果有空格，游戏没有结束
            if data[row][col] == 0:
                return False
            # 跳过障碍块
            if data[row][col] == -1:
                continue
            # 检查上下左右可以合并的情况
            # 上方相邻块
            if row > 0 and data[row - 1][col] == data[row][col]:
                return False
            # 下方相邻块
            if row < size - 1 and data[row + 1][col] == data[row][col]:
                return False
            # 左侧相邻块
            if col > 0 and data[row][col - 1] == data[row][col]:
                return False
            # 右侧相邻块
            if col < size - 1 and data[row][col + 1] == data[row][col]:
                return False
    # 如果没有空位且不存在可合并的方块，则游戏结束
    return True


#游戏失败信息
def show_game_over_message():
    screen.fill(GRAY)
    # 填充背景色
    screen.fill(GRAY)

    # 显示 "游戏结束" 文本
    game_over_text = solo_font.render("游戏失败！", True, RED)
    screen.blit(game_over_text, (130, 155))

    # 创建“新游戏”和“主菜单”按钮
    new_game_button = pygame.Rect(100, 300, 120, 50)
    main_menu_button = pygame.Rect(280, 300, 120, 50)
    re_game_button = pygame.Rect(190, 400, 120, 50)

    # 绘制“新游戏”按钮
    pygame.draw.rect(screen, BEIGE, new_game_button)
    new_game_text = re_font.render("新游戏", True, BLACK)
    screen.blit(new_game_text, (new_game_button.x + 20, new_game_button.y + 10))

    # 绘制“主菜单”按钮
    pygame.draw.rect(screen, BEIGE, main_menu_button)
    main_menu_text = re_font.render("主菜单", True, BLACK)
    screen.blit(main_menu_text, (main_menu_button.x + 20, main_menu_button.y + 10))

    # 绘制“复活”按钮
    pygame.draw.rect(screen, BEIGE, re_game_button)
    re_game_text = re_font.render("复活", True, BLACK)
    screen.blit(re_game_text, (main_menu_button.x - 60, main_menu_button.y + 110))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if new_game_button.collidepoint(x, y):
                    return "new_game"
                elif main_menu_button.collidepoint(x, y):
                    return "main_menu"
                elif re_game_button.collidepoint(x, y):
                    return "re_game"

    # 显示数学题
    problem, correct_answer = generate_math_problem()
    problem_text = re_font.render(problem, True, BLACK)
    screen.blit(problem_text, (150, 200))

    player_answer = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 玩家按下回车键提交答案
                    if verify_answer(player_answer, correct_answer):
                        # 复活成功，随机消除四个数并返回游戏数据
                        eliminate_random_tiles(game_data, 4)
                        return game_data  # 返回游戏数据以继续游戏
                    else:
                        # 复活失败，返回主菜单
                        return "main_menu"
                elif event.key == pygame.K_BACKSPACE:
                    # 删除最后一个字符（如果需要）
                    player_answer = player_answer[:-1]
                elif len(player_answer) < 3 and event.unicode.isdigit():
                    # 限制答案长度为3，且只接受数字字符
                    player_answer += event.unicode

        # 更新屏幕显示玩家答案
        answer_text = small_font.render(player_answer, True, BLACK)
        screen.blit(answer_text, (300, 200))
        pygame.display.flip()

# 显示测试
def show_test(problem, correct_answer):
    input_text = ""  # 初始化输入文本
    tiji_button = pygame.Rect(100, 320, 100, 50)  # 提交按钮的位置和大小
    while True:  # 开启一个无限循环
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检测是否点击了提交按钮
                if check_button_click(event.pos, tiji_button):
                    if input_text.isdigit() and int(input_text) == correct_answer:
                        return True  # 返回True，答案正确
                    else:
                        return False  # 返回False，答案错误

        # 处理输入事件并更新输入文本
        input_text = handle_input_events(event_list, input_text)

        # 清空屏幕
        screen.fill(GRAY)

        # 显示问题
        game_over_text = re_font.render("回答下列问题，复活：", True, BLACK)
        screen.blit(game_over_text, (100, 155))
        test_text = re_font.render(problem, True, BLACK)
        screen.blit(test_text, (100, 200))

        # 绘制输入框
        pygame.draw.rect(screen, WHITE, (100, 250, 200, 50))

        # 渲染并显示输入文本
        text_surface = re_font.render(input_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(100 + 200 // 2, 250 + 50 // 2))
        screen.blit(text_surface, text_rect)

        # 绘制提交按钮
        pygame.draw.rect(screen, BEIGE, tiji_button)
        tiji_text = re_font.render("提交", True, BLACK)
        screen.blit(tiji_text, (tiji_button.x + 20, tiji_button.y + 10))

        # 更新屏幕显示
        pygame.display.flip()

# 生成数学题
def generate_math_problem():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    problem = f"{num1} + {num2} = ?"
    correct_answer = num1 + num2
    return problem, correct_answer

# 获取输入框
def handle_input_events(event_list, input_text):
    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return input_text  # 返回输入的文本
            elif event.key == pygame.K_BACKSPACE:
                if input_text:  # 如果文本不为空，则删除最后一个字符
                    return input_text[:-1]
            else:
                if event.unicode and event.unicode.isprintable():  # 只接受可打印字符
                    return input_text + event.unicode
    return input_text

# 检测按钮点击
def check_button_click(pos, button_rect):
    if button_rect.collidepoint(pos):
        return True
    return False
#复活成功后随机消除数字快
def eliminate_random_tiles(game_data, count):
    size = game_data.size
    data = game_data.data
    eliminated = 0

    while eliminated < count:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if data[row][col] != 0 and data[row][col] != -1:  # 不消除障碍块
            data[row][col] = 0
            eliminated += 1
# 游戏循环
def game_loop(game_data):
    done = False
    while not done:
        draw_game(game_data)
        draw_back_button()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 10 <= x <= 90 and 10 <= y <= 50:
                    return
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP:
                    moved = move_up(game_data)
                elif event.key == pygame.K_DOWN:
                    moved = move_down(game_data)
                elif event.key == pygame.K_LEFT:
                    moved = move_left(game_data)
                elif event.key == pygame.K_RIGHT:
                    moved = move_right(game_data)
                # 仅在有有效移动时生成新数字并检查游戏结束
                if moved:
                    if is_game_over(game_data):
                        result = show_game_over_message()
                        if result == "new_game":
                            init_game(game_data)  # 开始新的游戏
                        elif result == "main_menu":
                            return  # 返回到主菜单
                        elif result == "re_game":
                            problem, correct_answer = generate_math_problem()
                            result1 = show_test(problem, correct_answer)
                            if result1:
                                eliminate_random_tiles(game_data, 4)  # 复活成功后随机消除四个数字块
                            else:
                                return
                    else:
                        generate_new_num(game_data)
                elif is_game_over(game_data):  # 如果没有移动且游戏已结束
                    result = show_game_over_message()
                    if result == "new_game":
                        init_game(game_data)
                    elif result == "main_menu":
                        return
                    elif result == "re_game":
                        problem, correct_answer = generate_math_problem()
                        result1 = show_test(problem, correct_answer)
                        if result1:
                            eliminate_random_tiles(game_data, 4)  # 复活成功后随机消除四个数字块
                        else:
                            return

# 主程序循环
while True:
    game_mode = show_menu()
    if game_mode is None:
        break
    if game_mode == "4x4":
        game_data = GameData(4)
    elif game_mode == "5x5":
        game_data = GameData(5)
    elif game_mode == "障碍模式":
        game_data = GameData(5, obstacles=True)
    init_game(game_data)
    game_loop(game_data)  # 进入游戏循环

pygame.quit()
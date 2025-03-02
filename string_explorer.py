import streamlit as st
import random
import time

# 设置页面配置
st.set_page_config(
    page_title="Python数字与字符串互动测验",
    page_icon="🐍",
    layout="wide"
)

# 添加CSS样式
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .question-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .feedback-correct {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .feedback-incorrect {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .explanation {
        background-color: #e2e3e5;
        color: #383d41;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .highlight {
        background-color: #ffc107;
        padding: 0 5px;
        border-radius: 3px;
    }
    .score-display {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 游戏问题数据 - 已修改，删除字节相关题目，增加更多数字和字符串题目
questions = [
    {
        "question": "在Python中，`5 / 2`的结果是什么？",
        "options": ["2", "2.5", "2.0", "Error"],
        "answer": 1,  # 索引从0开始，所以1代表第二个选项 "2.5"
        "explanation": "在Python 3中，`/`操作符总是执行浮点除法，返回浮点数结果，即使结果是整数。所以`5 / 2`的结果是`2.5`。如果想要执行整数除法（截断除法），应使用`//`操作符，例如`5 // 2`的结果是`2`。"
    },
    {
        "question": "Python中如何表示科学计数法？例如12300的科学记数法表示是？",
        "options": ["12.3 x 10^3", "1.23e4", "1.23 * 10**3", "12.3E+3"],
        "answer": 1,  # "1.23e4"
        "explanation": "在Python中，科学计数法使用`e`或`E`来表示10的幂。`1.23e4`表示1.23 × 10^4，等于12300。`e`后面的数字表示10的幂次。也可以使用`1.23E4`表示，效果相同。"
    },
    {
        "question": "以下哪个操作会报错？",
        "options": [
            "'Hello' + ' World'", 
            "'Hello' * 3", 
            "'Hello' - 'H'", 
            "'Hello'[1:3]"
        ],
        "answer": 2,  # "'Hello' - 'H'"
        "explanation": "Python中字符串可以进行连接（使用`+`）和重复（使用`*`），但不支持减法操作。所以`'Hello' - 'H'`会引发TypeError。而`'Hello'[1:3]`是一个切片操作，会返回`'el'`。"
    },
    {
        "question": "以下哪种方式可以将字符串'123'转换为整数123？",
        "options": ["int('123')", "float('123')", "str(123)", "eval('123')"],
        "answer": 0,  # "int('123')"
        "explanation": "`int('123')`将字符串'123'直接转换为整数123。虽然`float('123')`和`eval('123')`也能得到数值123，但`float()`会返回浮点数123.0，而`eval()`通常不推荐用于简单的类型转换，因为它可能会执行潜在的危险代码。`str(123)`是将整数123转换为字符串'123'，与题目要求相反。"
    },
    {
        "question": "以下关于Python字符串的说法，哪个是错误的？",
        "options": [
            "字符串是不可变的(immutable)", 
            "可以使用索引访问字符串中的字符", 
            "可以使用赋值语句修改字符串中的单个字符", 
            "可以使用切片操作获取子字符串"
        ],
        "answer": 2,  # "可以使用赋值语句修改字符串中的单个字符"
        "explanation": "Python中的字符串是不可变的(immutable)，这意味着一旦字符串被创建，就不能修改其内容。所以不能使用`s[0] = 'X'`这样的赋值语句修改字符串中的单个字符。如果需要修改字符串，必须创建一个新的字符串，例如`s = 'X' + s[1:]`。"
    },
    {
        "question": "以下哪个表达式的结果为False？",
        "options": ["0.1 + 0.2 > 0.3", "0.1 + 0.2 == 0.3", "0.1 + 0.2 >= 0.3", "int(0.1 + 0.2) == int(0.3)"],
        "answer": 1,  # "0.1 + 0.2 == 0.3"
        "explanation": "由于浮点数的精度问题，`0.1 + 0.2`的结果实际上是约0.30000000000000004，而不是精确的0.3。因此，`0.1 + 0.2 == 0.3`的结果是False。当比较浮点数时，应避免使用精确相等，而应使用一个小的误差范围，例如`abs(0.1 + 0.2 - 0.3) < 1e-10`。"
    },
    {
        "question": "执行以下代码后的输出是什么？\n```python\nprint(f\"{3.14159:.2f}\")\n```",
        "options": ["3.14159", "3.14", "3", "Error"],
        "answer": 1,  # "3.14"
        "explanation": "f-字符串格式说明符`.2f`表示将浮点数格式化为保留2位小数。所以`f\"{3.14159:.2f}\"`会输出`\"3.14\"`。这是Python 3.6+引入的f-字符串特性，提供了一种简洁的字符串格式化方式。"
    },
    {
        "question": "下面的表达式`round(2.5)`的结果是什么？",
        "options": ["2", "3", "2.5", "Error"],
        "answer": 0,  # "2"
        "explanation": "在Python 3中，`round()`函数使用'银行家舍入法'，当一个数字距离两个整数同样远时（如2.5距离2和3同样远），会舍入到最近的偶数。所以`round(2.5)`结果是`2`，而`round(3.5)`结果是`4`。这与许多人期望的传统四舍五入规则不同。"
    },
    {
        "question": "在Python中，字符串的切片操作`s[::-1]`的作用是什么？",
        "options": ["返回原字符串", "删除字符串的第一个字符", "反转字符串", "去除字符串两端的空白"],
        "answer": 2,  # "反转字符串"
        "explanation": "字符串切片`s[::-1]`中，第三个参数-1表示步长为-1，即从后向前取字符。这个操作会返回原字符串的反转版本。例如，如果`s = 'hello'`，那么`s[::-1]`的结果是`'olleh'`。"
    },
    {
        "question": "以下哪个方法可以检查字符串是否以特定子串开头？",
        "options": ["startswith()", "beginswith()", "prefix()", "starts()"],
        "answer": 0,  # "startswith()"
        "explanation": "Python字符串的`startswith()`方法用于检查字符串是否以指定的子串开头。例如，`'Hello'.startswith('He')`返回`True`。相应地，`endswith()`方法用于检查字符串是否以指定的子串结尾。"
    },
    {
        "question": "执行以下代码后的结果是什么？\n```python\nlist(map(int, '123'))\n```",
        "options": ["[123]", "[1, 2, 3]", "['1', '2', '3']", "Error"],
        "answer": 1,  # "[1, 2, 3]"
        "explanation": "`map(int, '123')`将`int`函数应用到可迭代对象`'123'`的每个元素上。字符串是可迭代的，迭代时产生其每个字符，所以结果是将字符'1'、'2'、'3'分别转换为整数1、2、3。最后用`list()`将map对象转换为列表，得到`[1, 2, 3]`。"
    },
    {
        "question": "以下哪种方法可以将列表['a', 'b', 'c']转换为字符串'a,b,c'？",
        "options": [
            "','.join(['a', 'b', 'c'])", 
            "str(['a', 'b', 'c'])", 
            "['a', 'b', 'c'].toString()", 
            "convert(['a', 'b', 'c'], ',')"
        ],
        "answer": 0,  # "','.join(['a', 'b', 'c'])"
        "explanation": "在Python中，要将列表元素连接成一个字符串，应使用字符串的`join()`方法。该方法的语法是`分隔符.join(可迭代对象)`，它将可迭代对象中的每个元素转换为字符串，然后用分隔符连接起来。所以`','.join(['a', 'b', 'c'])`的结果是`'a,b,c'`。"
    },
    {
        "question": "如果`x = 5`，以下哪个f-字符串表达式会显示'x = 5'？",
        "options": ["f'x = {x}'", "f'{x} = 5'", "f'{x=}'", "f'x = x'"],
        "answer": 2,  # "f'{x=}'"
        "explanation": "在Python 3.8及以上版本中，f-字符串引入了一个调试特性：在表达式后加上等号`=`，会同时显示变量名和其值。所以当`x = 5`时，`f'{x=}'`会显示`'x=5'`。这是一个非常方便的特性，可以快速查看变量的值，特别适合调试时使用。"
    },
    {
        "question": "以下哪个位运算表达式的结果等于18？",
        "options": ["4 << 2", "9 << 1", "36 >> 1", "5 | 16"],
        "answer": 1,  # "9 << 1"
        "explanation": "位运算符`<<`表示左移，将二进制位向左移动指定的位数，右边用0填充。左移1位相当于乘以2。\n- `9`的二进制是`1001`，左移1位后变成`10010`，即十进制的18。\n- `4 << 2`是将4左移2位，结果是16。\n- `36 >> 1`是将36右移1位，结果是18。\n- `5 | 16`是按位或操作，结果是21。"
    },
    {
        "question": "以下哪个表达式正确计算了字符串中非空格字符的数量？",
        "options": [
            "len(s.strip())", 
            "len(s) - s.count(' ')", 
            "sum(1 for c in s if c != ' ')", 
            "len(s.replace(' ', ''))"
        ],
        "answer": 3,  # "len(s.replace(' ', ''))"
        "explanation": "要计算字符串中非空格字符的数量，可以先使用`replace()`方法将所有空格替换为空字符串，然后计算结果字符串的长度。`s.strip()`只会移除字符串两端的空白，而不会移除中间的空白。`len(s) - s.count(' ')`可以计算非空格字符的数量，但如果字符串中包含其他空白字符（如制表符、换行符），结果会不准确。"
    },
    {
        "question": "如何获取字符串'Python'的最后三个字符？",
        "options": [
            "'Python'[-3:]", 
            "'Python'[3:6]", 
            "'Python'[-3:-1]", 
            "'Python'[3:]"
        ],
        "answer": 0,  # "'Python'[-3:]"
        "explanation": "使用切片`s[-3:]`可以获取字符串`s`的最后三个字符。这里`-3`表示从末尾开始的第三个字符，省略第二个参数表示一直切到字符串末尾。对于字符串'Python'，`'Python'[-3:]`返回'hon'。\n- `'Python'[3:6]`返回'hon'，但这种方式依赖于字符串的长度，不够灵活。\n- `'Python'[-3:-1]`返回'ho'，不包括最后一个字符。\n- `'Python'[3:]`返回'hon'，但同样依赖于字符串的长度。"
    }
]

# 初始化会话状态
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'questions_shuffled' not in st.session_state:
    st.session_state.questions_shuffled = random.sample(questions, len(questions))
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# 重置游戏
def reset_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.game_over = False
    st.session_state.questions_shuffled = random.sample(questions, len(questions))
    st.session_state.start_time = time.time()

# 下一题或完成测验
def next_question():
    if st.session_state.current_question < len(st.session_state.questions_shuffled) - 1:
        st.session_state.current_question += 1
        st.session_state.answered = False
        st.session_state.selected_option = None
    else:
        st.session_state.game_over = True
        st.session_state.end_time = time.time()

# 主页面
def main():
    st.markdown("<div class='header'><h1>🐍 Python数字与字符串互动测验 🔢</h1></div>", unsafe_allow_html=True)
    
    if st.session_state.game_over:
        elapsed_time = st.session_state.end_time - st.session_state.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        
        st.markdown(f"<div class='score-display'>🎉 测验完成! 你的得分: {st.session_state.score}/{len(questions)} ({st.session_state.score / len(questions) * 100:.0f}%)</div>", unsafe_allow_html=True)
        st.markdown(f"<div>完成时间: {int(minutes)}分钟 {int(seconds)}秒</div>", unsafe_allow_html=True)
        
        # 根据分数给出评价
        if st.session_state.score >= 13:
            st.success("太棒了！你对Python的数字和字符串知识掌握得非常好！")
        elif st.session_state.score >= 10:
            st.info("不错！你对Python的数字和字符串有很好的理解，继续努力！")
        elif st.session_state.score >= 7:
            st.warning("加油！你已经掌握了一些基础知识，但还需要更多的练习。")
        else:
            st.error("建议再复习一下Python的数字和字符串基础知识，不要气馁，继续加油！")
        
        if st.button("再来一次"):
            reset_game()
    else:
        # 显示进度和分数
        st.progress((st.session_state.current_question + 1) / len(questions))
        st.markdown(f"<div>问题 {st.session_state.current_question + 1}/{len(questions)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='score-display'>当前得分: {st.session_state.score}/{st.session_state.current_question}</div>", unsafe_allow_html=True)
        
        # 获取当前问题
        current_q = st.session_state.questions_shuffled[st.session_state.current_question]
        
        # 显示问题
        st.markdown(f"<div class='question-container'><h3>{current_q['question']}</h3></div>", unsafe_allow_html=True)
        
        # 选项
        option_labels = ["A", "B", "C", "D"]
        selected_idx = None
        
        # 如果还没回答，显示选项并接受输入
        if not st.session_state.answered:
            for i, option in enumerate(current_q['options']):
                if st.button(f"{option_labels[i]}. {option}", key=f"option_{i}"):
                    st.session_state.answered = True
                    st.session_state.selected_option = i
                    if i == current_q['answer']:
                        st.session_state.score += 1
            
            # 添加一个"跳过"按钮
            if st.button("跳过这个问题"):
                st.session_state.answered = True
                st.session_state.selected_option = None
        else:
            # 已经回答了，显示选中的选项和正确答案
            for i, option in enumerate(current_q['options']):
                if i == st.session_state.selected_option:
                    if i == current_q['answer']:
                        st.markdown(f"<div style='background-color: #d4edda; padding: 10px; border-radius: 5px;'>{option_labels[i]}. {option} ✓</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px;'>{option_labels[i]}. {option} ✗</div>", unsafe_allow_html=True)
                elif i == current_q['answer']:
                    st.markdown(f"<div style='background-color: #d4edda; padding: 10px; border-radius: 5px;'>{option_labels[i]}. {option} ✓</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{option_labels[i]}. {option}")
            
            # 显示解释
            st.markdown(f"<div class='explanation'><h4>解释:</h4>{current_q['explanation']}</div>", unsafe_allow_html=True)
            
            # 下一题按钮
            if st.button("下一题"):
                next_question()
    
    # 显示页脚
    st.markdown("---")
    st.markdown("Python数字与字符串互动测验 | 通过Streamlit实现 | 2025")

if __name__ == "__main__":
    main()
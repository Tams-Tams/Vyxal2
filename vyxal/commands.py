from typing import Callable, Tuple, List, Union

from vyxal.builtins import *
from vyxal.array_builtins import *
from vyxal.utilities import *

codepage = "λƛ¬∧⟑∨⟇÷×«\n»°•ß†€"
codepage += "½∆ø↔¢⌐æʀʁɾɽÞƈ∞¨ "
codepage += "!\"#$%&'()*+,-./01"
codepage += "23456789:;<=>?@A"
codepage += "BCDEFGHIJKLMNOPQ"
codepage += "RSTUVWXYZ[\\]`^_abc"
codepage += "defghijklmnopqrs"
codepage += "tuvwxyz{|}~↑↓∴∵›"
codepage += "‹∷¤ð→←βτȧḃċḋėḟġḣ"
codepage += "ḭŀṁṅȯṗṙṡṫẇẋẏż√⟨⟩"
codepage += "‛₀₁₂₃₄₅₆₇₈¶⁋§ε¡"
codepage += "∑¦≈µȦḂĊḊĖḞĠḢİĿṀṄ"
codepage += "ȮṖṘṠṪẆẊẎŻ₌₍⁰¹²∇⌈"
codepage += "⌊¯±₴…□↳↲⋏⋎꘍ꜝ℅≤≥"
codepage += "≠⁼ƒɖ∪∩⊍£¥⇧⇩ǍǎǏǐǑ"
codepage += "ǒǓǔ⁽‡≬⁺↵⅛¼¾Π„‟"

assert len(codepage) == 256


def make_cmd(
    to_fn_call: Union[str, Callable[[List[str]], str]], arity: int
) -> Tuple[str, int]:
    """
    Returns a tuple with the transpiled command and its arity.

    :param to_fn_call
      If Callable, takes a list of variables that hold values popped from the
      stack (reversed) and returns a string representing a value created by
      running some function.
      If str, its format method will be called with the aforementioned list
      of variables as arguments.
    on those variables
    :param arity The arity of the function
    """
    var_names = [f"x{n}" for n in range(arity, 0, -1)]
    if isinstance(to_fn_call, str):
        fn_call = to_fn_call.format(*var_names)
    else:
        fn_call = to_fn_call(var_names)
    if arity > 0:
        cmd = f"{', '.join(var_names[::-1])} = pop(vy_globals.stack, {arity});"
    else:
        cmd = ""
    cmd += f"res = {fn_call}; vy_globals.stack.append(res);"
    return cmd, arity


def fn_to_cmd(fn: Union[Callable, str], arity: int) -> Tuple[str, int]:
    """
    Returns a tuple with the transpiled command and its arity.

    :param fn The function to turn into a command, or its name
    :param arity The arity of the function
    """
    fn_name = fn if isinstance(fn, str) else fn.__name__
    return make_cmd(lambda var_names: f"{fn_name}({', '.join(var_names)})", arity)


command_dict = {
    "¬": make_cmd("not {}", 1),
    "∧": make_cmd("{} and {}", 2),
    "⟑": make_cmd("{1} and {0}", 2),
    "∨": make_cmd("{} or {}", 2),
    "⟇": make_cmd("{1} or {0}", 2),
    "÷": (
        "for item in iterable(pop(vy_globals.stack)): vy_globals.stack.append(item)",
        1,
    ),
    "•": fn_to_cmd(log, 2),
    "†": (
        "fn = pop(vy_globals.stack); vy_globals.stack += function_call(fn, vy_globals.stack)",
        1,
    ),
    "€": fn_to_cmd(split, 2),
    "½": fn_to_cmd(halve, 1),
    "↔": fn_to_cmd(combinations_replace_generate, 2),
    "⌐": fn_to_cmd(complement, 1),
    "æ": fn_to_cmd(is_prime, 1),
    "ʀ": (
        "vy_globals.stack.append(orderless_range(0, add(pop(vy_globals.stack), 1)))",
        1,
    ),
    "ʁ": make_cmd("orderless_range(0, {})", 1),
    "ɾ": (
        "vy_globals.stack.append(orderless_range(1, add(pop(vy_globals.stack), 1)))",
        1,
    ),
    "ɽ": make_cmd("orderless_range(1, {})", 1),
    "ƈ": fn_to_cmd(ncr, 2),
    "∞": make_cmd("non_negative_integers()", 0),
    "!": make_cmd("len(vy_globals.stack)", 0),
    '"': make_cmd("[{}, {}]", 2),
    "$": (
        "top, over = pop(vy_globals.stack, 2);"
        "vy_globals.stack.append(top);"
        "vy_globals.stack.append(over)",
        2,
    ),
    "%": fn_to_cmd(modulo, 2),
    "*": fn_to_cmd(multiply, 2),
    "+": fn_to_cmd(add, 2),
    ",": ("vy_print(pop(vy_globals.stack))", 1),
    "-": fn_to_cmd(subtract, 2),
    "/": fn_to_cmd(divide, 2),
    ":": (
        "temp = pop(vy_globals.stack);"
        "vy_globals.stack.append(temp);"
        "vy_globals.stack.append(deref(temp))",
        1,
    ),
    "^": ("vy_globals.stack = vy_globals.stack[::-1]", 0),
    "_": ("pop(vy_globals.stack)", 1),
    "<": make_cmd("compare({}, {}, Comparitors.LESS_THAN)", 2),
    ">": make_cmd("compare({}, {}, Comparitors.GREATER_THAN)", 2),
    "=": make_cmd("compare({}, {}, Comparitors.EQUALS)", 2),
    "?": make_cmd("get_input(0)", 0),
    "A": make_cmd("int(all(iterable({})))", 1),
    "B": make_cmd("vy_int({}, 2)", 1),
    "C": fn_to_cmd(chrord, 1),
    "D": (
        "temp = pop(vy_globals.stack);"
        "vy_globals.stack.append(temp);"
        "vy_globals.stack.append(deref(temp));"
        "vy_globals.stack.append(deref(vy_globals.stack[-1]))",
        1,
    ),
    "E": fn_to_cmd(vy_eval, 1),
    "F": make_cmd("vy_filter({1}, {0})", 2),
    "G": make_cmd("vy_max(iterable({}))", 1),
    "H": make_cmd("vy_int({}, 16)", 1),
    "I": fn_to_cmd(vy_int, 1),
    "J": fn_to_cmd(join, 2),
    "K": fn_to_cmd(divisors_of, 1),
    "L": (
        "top = pop(vy_globals.stack); vy_globals.stack.append(len(iterable(top)))",
        1,
    ),
    "M": (
        "fn, vector = pop(vy_globals.stack, 2); temp = vy_map(fn, vector); vy_globals.stack.append(temp)",
        2,
    ),
    "N": fn_to_cmd(negate, 1),
    "O": (
        "needle, haystack = pop(vy_globals.stack, 2); vy_globals.stack.append(iterable(haystack).count(needle))",
        2,
    ),
    "P": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(vy_str(lhs).strip(vy_str(rhs)))",
        2,
    ),
    "Q": ("exit()", 0),
    "R": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack += vy_reduce(fn, vector)",
        2,
    ),
    "S": fn_to_cmd(vy_str, 1),
    "T": (
        "vy_globals.stack.append([i for (i, x) in enumerate(pop(vy_globals.stack)) if bool(x)])",
        1,
    ),
    "U": ("vy_globals.stack.append(Generator(uniquify(pop(vy_globals.stack))))", 1),
    "V": fn_to_cmd(replace, 3),
    "W": ("vy_globals.stack = [deref(vy_globals.stack)]; print(vy_globals.stack)", 0),
    "X": ("context_level += 1", 0),
    "Y": fn_to_cmd(interleave, 2),
    "Z": (
        "rhs, lhs = pop(vy_globals.stack, 2);"
        "vy_globals.stack.append(Generator(vy_zip(iterable(lhs), iterable(rhs))))",
        2,
    ),
    "a": ("vy_globals.stack.append(int(any(iterable(pop(vy_globals.stack)))))", 1),
    "b": fn_to_cmd(vy_bin, 1),
    "c": (
        "needle, haystack = pop(vy_globals.stack, 2);"
        "haystack = iterable(haystack, str)\n"
        "if type(haystack) is str: needle = vy_str(needle)\n"
        "vy_globals.stack.append(int(needle in iterable(haystack, str)))",
        2,
    ),
    "d": ("vy_globals.stack.append(multiply(pop(vy_globals.stack), 2))", 1),
    "e": fn_to_cmd(exponate, 2),
    "f": ("vy_globals.stack.append(flatten(iterable(pop(vy_globals.stack))))", 1),
    "g": ("vy_globals.stack.append(vy_min(iterable(pop(vy_globals.stack))))", 1),
    "h": ("vy_globals.stack.append(iterable(pop(vy_globals.stack))[0])", 1),
    "i": fn_to_cmd(index, 2),
    "j": fn_to_cmd(join_on, 2),
    "l": fn_to_cmd(nwise_pair, 2),
    "m": fn_to_cmd(mirror, 1),
    "n": (
        "vy_globals.stack.append(context_values[context_level % len(context_values)])",
        0,
    ),
    "o": fn_to_cmd(remove, 2),
    "p": fn_to_cmd(prepend, 2),
    "q": fn_to_cmd(uneval, 1),
    "r": fn_to_cmd(orderless_range, 2),
    "s": fn_to_cmd(vy_sorted, 1),
    "t": ("vy_globals.stack.append(iterable(pop(vy_globals.stack))[-1])", 1),
    "u": ("vy_globals.stack.append(-1)", 0),
    "w": ("vy_globals.stack.append([pop(vy_globals.stack)])", 1),
    "x": ("vy_globals.stack += this_function(vy_globals.stack)", 0),
    "y": ("vy_globals.stack += uninterleave(pop(vy_globals.stack))", 1),
    "z": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack += vy_zipmap(fn, vector)",
        2,
    ),
    "↑": (
        "vy_globals.stack.append(max(pop(vy_globals.stack), key=lambda x: x[-1]))",
        1,
    ),
    "↓": (
        "vy_globals.stack.append(min(pop(vy_globals.stack), key=lambda x: x[-1]))",
        1,
    ),
    "∴": fn_to_cmd(vy_max, 2),
    "∵": fn_to_cmd(vy_min, 2),
    "β": (
        "alphabet, number = pop(vy_globals.stack, 2); vy_globals.stack.append(utilities.to_ten(number, alphabet))",
        2,
    ),
    "τ": (
        "alphabet, number = pop(vy_globals.stack, 2); vy_globals.stack.append(utilities.from_ten(number, alphabet))",
        2,
    ),
    "›": ("vy_globals.stack.append(add(pop(vy_globals.stack), 1))", 1),
    "‹": ("vy_globals.stack.append(subtract(pop(vy_globals.stack), 1))", 1),
    "∷": ("vy_globals.stack.append(modulo(pop(vy_globals.stack), 2))", 1),
    "¤": ("vy_globals.stack.append('')", 0),
    "ð": ("vy_globals.stack.append(' ')", 0),
    "ȧ": fn_to_cmd(vy_abs, 1),
    "ḃ": (
        "vy_globals.stack.append(int(not compare(pop(vy_globals.stack), 0, Comparitors.EQUALS)))",
        1,
    ),
    "ċ": (
        "vy_globals.stack.append(compare(pop(vy_globals.stack), 1, Comparitors.NOT_EQUALS))",
        1,
    ),
    "ḋ": fn_to_cmd(
        vy_divmod, 2
    ),  # Dereference because generators could accidentally get exhausted.
    "ė": (
        "vy_globals.stack.append(Generator(enumerate(iterable(pop(vy_globals.stack)))))",
        1,
    ),
    "ḟ": fn_to_cmd(find, 2),
    "ġ": (
        "rhs = pop(vy_globals.stack)\nif vy_type(rhs) in [list, Generator]: vy_globals.stack.append(gcd(rhs))\nelse: vy_globals.stack.append(gcd(pop(vy_globals.stack), rhs))",
        2,
    ),
    "ḣ": (
        "top = iterable(pop(vy_globals.stack)); vy_globals.stack.append(top[0]); vy_globals.stack.append(top[1:])",
        1,
    ),
    "ḭ": fn_to_cmd(integer_divide, 2),
    "ŀ": (
        "start, needle, haystack = pop(vy_globals.stack, 3); vy_globals.stack.append(find(haystack, needle, start))",
        3,
    ),
    "ṁ": (
        "top = iterable(pop(vy_globals.stack)); vy_globals.stack.append(divide(summate(top), len(top)))",
        1,
    ),
    "ṅ": fn_to_cmd(first_n, 1),
    "ȯ": fn_to_cmd(first_n, 2),
    "ṗ": ("vy_globals.stack.append(powerset(iterable(pop(vy_globals.stack))))", 1),
    "ṙ": fn_to_cmd(vy_round, 1),
    "ṡ": (
        "fn , vector = pop(vy_globals.stack, 2); vy_globals.stack.append(vy_sorted(vector, fn))",
        2,
    ),
    "ṫ": (
        "vector = iterable(pop(vy_globals.stack)); vy_globals.stack.append(vector[:-1]); vy_globals.stack.append(vector[-1])",
        1,
    ),
    "ẇ": fn_to_cmd(wrap, 2),
    "ẋ": (
        "rhs, lhs = pop(vy_globals.stack, 2); main = None;\nif vy_type(lhs) is Function: main = pop(vy_globals.stack)\nvy_globals.stack.append(repeat(lhs, rhs, main))",
        2,
    ),
    "ẏ": (
        "obj = iterable(pop(vy_globals.stack)); vy_globals.stack.append(Generator(range(0, len(obj))))",
        1,
    ),
    "ż": (
        "obj = iterable(pop(vy_globals.stack)); vy_globals.stack.append(Generator(range(1, len(obj) + 1)))",
        1,
    ),
    "√": ("vy_globals.stack.append(exponate(pop(vy_globals.stack), 0.5))", 1),
    "₀": ("vy_globals.stack.append(10)", 0),
    "₁": ("vy_globals.stack.append(100)", 0),
    "₂": (
        "vy_globals.stack.append(const_divisibility(pop(vy_globals.stack), 2, lambda item: len(item) % 2 == 0))",
        1,
    ),
    "₃": (
        "vy_globals.stack.append(const_divisibility(pop(vy_globals.stack), 3, lambda item: len(item) == 1))",
        1,
    ),
    "₄": ("vy_globals.stack.append(26)", 0),
    "₅": (
        "top = pop(vy_globals.stack); res = const_divisibility(top, 5, lambda item: (top, len(item)))\nif type(res) is tuple: vy_globals.stack += list(res)\nelse: vy_globals.stack.append(res)",
        1,
    ),
    "₆": ("vy_globals.stack.append(64)", 0),
    "₇": ("vy_globals.stack.append(128)", 0),
    "₈": ("vy_globals.stack.append(256)", 0),
    "¶": ("vy_globals.stack.append('\\n')", 0),
    "⁋": fn_to_cmd(osabie_newline_join, 1),
    "§": fn_to_cmd(vertical_join, 1),
    "ε": fn_to_cmd(vertical_join, 2),
    "¡": fn_to_cmd(factorial, 1),
    "∑": (
        "temp = summate(pop(vy_globals.stack));vy_globals.stack.append(temp);print(vy_globals.stack);",
        1,
    ),
    "¦": (
        "vy_globals.stack.append(cumulative_sum(iterable(pop(vy_globals.stack))))",
        1,
    ),
    "≈": (
        "vy_globals.stack.append(int(len(set(iterable(pop(vy_globals.stack)))) == 1))",
        1,
    ),
    "Ȧ": (
        "value, lst_index, vector = pop(vy_globals.stack, 3); vy_globals.stack.append(assigned(iterable(vector), lst_index, value))",
        3,
    ),
    "Ḃ": ("vy_globals.stack += bifurcate(pop(vy_globals.stack))", 1),
    "Ċ": fn_to_cmd(counts, 1),
    "Ḋ": (
        "rhs, lhs = pop(vy_globals.stack, 2); ret = is_divisble(lhs, rhs)\nif type(ret) is tuple: vy_globals.stack += list(ret)\nelse: vy_globals.stack.append(ret)",
        2,
    ),
    "Ė": ("vy_globals.stack += vy_exec(pop(vy_globals.stack))", 1),
    "Ḟ": (
        """top = pop(vy_globals.stack)
if vy_type(top) is Number:
    limit = int(top); vector = pop(vy_globals.stack)
else:
    limit = -1; vector = top
fn = pop(vy_globals.stack)
vy_globals.stack.append(Generator(fn, limit=limit, initial=iterable(vector)))
""",
        2,
    ),
    "Ġ": (
        "vy_globals.stack.append(group_consecutive(iterable(pop(vy_globals.stack))))",
        1,
    ),
    "Ḣ": ("vy_globals.stack.append(iterable(pop(vy_globals.stack))[1:])", 1),
    "İ": fn_to_cmd(indexed_into, 2),
    "Ŀ": (
        "new, original, value = pop(vy_globals.stack, 3)\nif Function in map(type, (new, original, value)): vy_globals.stack.append(repeat_no_collect(value, original, new))\nelse: vy_globals.stack.append(transliterate(iterable(original, str), iterable(new, str), iterable(value, str)))",
        3,
    ),
    "Ṁ": (
        "item, index, vector = pop(vy_globals.stack, 3);\nif Function in map(type, (item, index, vector)): vy_globals.stack.append(map_every_n(vector, item, index))\nelse: vy_globals.stack.append(inserted(vector, item, index))",
        3,
    ),
    "Ṅ": (
        "top = pop(vy_globals.stack);\nif vy_type(top) == Number:vy_globals.stack.append(Generator(partition(top)))\nelse: vy_globals.stack.append(' '.join([vy_str(x) for x in top]))",
        1,
    ),  # ---------------------------
    "Ȯ": (
        "if len(vy_globals.stack) >= 2: vy_globals.stack.append(vy_globals.stack[-2])\nelse: vy_globals.stack.append(get_input(0))",
        0,
    ),
    "Ṗ": (
        "vy_globals.stack.append(Generator(permutations(iterable(pop(vy_globals.stack)))))",
        1,
    ),
    "Ṙ": fn_to_cmd(reverse, 1),
    "Ṡ": ("vy_globals.stack = [summate(vy_globals.stack)]", 0),
    "Ṫ": ("vy_globals.stack.append(iterable(pop(vy_globals.stack), str)[:-1])", 1),
    "Ẇ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(split(lhs, rhs, True))",
        2,
    ),
    "Ẋ": fn_to_cmd(cartesian_product, 2),
    "Ẏ": (
        "index, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(one_argument_tail_index(vector, index, 0))",
        2,
    ),
    "Ż": (
        "index, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(one_argument_tail_index(vector, index, 1))",
        2,
    ),
    "⁰": ("vy_globals.stack.append(input_values[0][0][-1])", 0),
    "¹": ("vy_globals.stack.append(input_values[0][0][-2])", 0),
    "²": ("x = pop(vy_globals.stack); vy_globals.stack.append(square(x))", 1),
    "∇": (
        "c, b, a = pop(vy_globals.stack, 3); vy_globals.stack.append(c); vy_globals.stack.append(a); vy_globals.stack.append(b)",
        3,
    ),
    "⌈": fn_to_cmd(ceiling, 1),
    "⌊": fn_to_cmd(floor, 1),
    "¯": fn_to_cmd(deltas, 1),
    "±": fn_to_cmd(sign_of, 1),
    "₴": ("vy_print(pop(vy_globals.stack), end='')", 1),
    "…": (
        "top = pop(vy_globals.stack); vy_globals.stack.append(top); vy_print(top)",
        0,
    ),
    "□": (
        "if inputs: vy_globals.stack.append(inputs)\nelse:\n    s, x = [], input()\n    while x:\n        s.append(vy_eval(x)); x = input()",
        0,
    ),
    "↳": fn_to_cmd(rshift, 2),
    "↲": fn_to_cmd(lshift, 2),
    "⋏": fn_to_cmd(bit_and, 2),
    "⋎": fn_to_cmd(bit_or, 2),
    "꘍": fn_to_cmd(bit_xor, 2),
    "ꜝ": fn_to_cmd(bit_not, 1),
    "℅": ("vy_globals.stack.append(random.choice(iterable(pop(vy_globals.stack))))", 1),
    "≤": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(compare(lhs, rhs, Comparitors.LESS_THAN_EQUALS))",
        2,
    ),
    "≥": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(compare(lhs, rhs, Comparitors.GREATER_THAN_EQUALS))",
        2,
    ),
    "≠": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(int(deref(lhs) != deref(rhs)))",
        2,
    ),
    "⁼": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(int(deref(lhs) == deref(rhs)))",
        2,
    ),
    "ƒ": fn_to_cmd(fractionify, 1),
    "ɖ": fn_to_cmd(decimalify, 1),
    "×": ("vy_globals.stack.append('*')", 0),
    "∪": fn_to_cmd(set_union, 2),
    "∩": fn_to_cmd(set_intersection, 2),
    "⊍": fn_to_cmd(set_caret, 2),
    "£": ("register = pop(vy_globals.stack)", 1),
    "¥": ("vy_globals.stack.append(register)", 0),
    "⇧": fn_to_cmd(graded, 1),
    "⇩": fn_to_cmd(graded_down, 1),
    "Ǎ": fn_to_cmd(two_power, 1),
    "ǎ": fn_to_cmd(nth_prime, 1),
    "Ǐ": fn_to_cmd(prime_factors, 1),
    "ǐ": fn_to_cmd(all_prime_factors, 1),
    "Ǒ": fn_to_cmd(order, 2),
    "ǒ": fn_to_cmd(is_empty, 1),
    "Ǔ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack += overloaded_iterable_shift(lhs, rhs, ShiftDirections.LEFT)",
        2,
    ),
    "ǔ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack += overloaded_iterable_shift(lhs, rhs, ShiftDirections.RIGHT)",
        2,
    ),
    "¢": (
        "replacement, needle, haystack = pop(vy_globals.stack, 3); vy_globals.stack.append(infinite_replace(haystack, needle, replacement))",
        3,
    ),
    "↵": fn_to_cmd(split_newlines_or_pow_10, 1),
    "⅛": ("global_stack.append(pop(vy_globals.global_stack))", 1),
    "¼": ("vy_globals.stack.append(pop(vy_globals.global_stack))", 0),
    "¾": ("vy_globals.stack.append(deref(vy_globals.global_stack))", 0),
    "Π": ("vy_globals.stack.append(product(iterable(pop(vy_globals.stack))))", 1),
    "„": (
        "vy_globals.stack = iterable_shift(vy_globals.stack, ShiftDirections.LEFT)",
        0,
    ),
    "‟": (
        "vy_globals.stack = iterable_shift(vy_globals.stack, ShiftDirections.RIGHT)",
        0,
    ),
    "∆S": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.asin, arg))",
        1,
    ),
    "∆C": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.acos, arg))",
        1,
    ),
    "∆T": ("arg = pop(vy_globals.stack); vy_globals.stack.append(math.atan(arg))", 1),
    "∆q": (
        "coeff_a, coeff_b = pop(vy_globals.stack, 2); vy_globals.stack.append(polynomial([coeff_a, coeff_b, 0]))",
        2,
    ),
    "∆Q": (
        "coeff_b, coeff_c = pop(vy_globals.stack, 2); vy_globals.stack.append(polynomial([1, coeff_b, coeff_c]))",
        2,
    ),
    "∆P": (
        "coeff = iterable(pop(vy_globals.stack)); vy_globals.stack.append(polynomial(coeff));",
        1,
    ),
    "∆s": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.sin, arg))",
        1,
    ),
    "∆c": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.cos, arg))",
        1,
    ),
    "∆t": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.tan, arg))",
        1,
    ),
    "∆ƈ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(divide(factorial(lhs), factorial(subtract(lhs, rhs))))",
        2,
    ),
    "∆±": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(vectorise(math.copysign, lhs, rhs))",
        2,
    ),
    "∆K": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(summate(join(0, divisors_of(arg)[:-1])))",
        1,
    ),
    "∆²": ("arg = pop(vy_globals.stack); vy_globals.stack.append(is_square(arg))", 1),
    "∆e": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.exp, arg))",
        1,
    ),
    "∆E": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.expm1, arg))",
        1,
    ),
    "∆L": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.log, arg))",
        1,
    ),
    "∆l": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.log2, arg))",
        1,
    ),
    "∆τ": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.log10, arg))",
        1,
    ),
    "∆d": fn_to_cmd(distance_between, 2),
    "∆D": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.degrees, arg))",
        1,
    ),
    "∆R": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(vectorise(math.radians, arg))",
        1,
    ),
    "∆≤": (
        "arg = pop(vy_globals.stack); vy_globals.stack.append(compare(vy_abs(arg), 1, Comparitors.LESS_THAN_EQUALS))",
        1,
    ),
    "∆Ṗ": fn_to_cmd(next_prime, 1),
    "∆ṗ": fn_to_cmd(prev_prime, 1),
    "∆p": fn_to_cmd(closest_prime, 1),
    "∆ṙ": (
        "vy_globals.stack.append(unsympy(sympy.prod(map(sympy.poly('x').__sub__, iterable(pop(vy_globals.stack)))).all_coeffs()[::-1]))",
        1,
    ),
    "∆Ṙ": ("vy_globals.stack.append(random.random())", 0),
    "∆W": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(vectorise(round, lhs, rhs))",
        2,
    ),  # if you think I'm making this work with strings, then you can go commit utter go awayance. smh.
    "∆Ŀ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(vectorise(lambda x, y: int(numpy.lcm(x, y)), lhs, rhs))",
        2,
    ),
    "øo": (
        "needle, haystack = pop(vy_globals.stack, 2); vy_globals.stack.append(infinite_replace(haystack, needle, ''))",
        2,
    ),
    "øV": (
        "replacement, needle, haystack = pop(vy_globals.stack, 3); vy_globals.stack.append(infinite_replace(haystack, needle, replacement))",
        3,
    ),
    "øc": (
        "value = pop(vy_globals.stack); vy_globals.stack.append('«' + utilities.from_ten(utilities.to_ten(value, utilities.base27alphabet), encoding.codepage_string_compress) + '«')",
        1,
    ),
    "øC": (
        "number = pop(vy_globals.stack); vy_globals.stack.append('»' + utilities.from_ten(number, encoding.codepage_number_compress) + '»')",
        1,
    ),
    "øĊ": fn_to_cmd(centre, 1),
    "øm": ("vy_globals.stack.append(palindromise(iterable(pop(vy_globals.stack))))", 1),
    "øe": (
        "vy_globals.stack.append(run_length_encode(iterable(pop(vy_globals.stack), str)))",
        1,
    ),
    "ød": fn_to_cmd(run_length_decode, 1),
    "øD": fn_to_cmd(dictionary_compress, 1),
    "øW": ("vy_globals.stack.append(split_on_words(vy_str(pop(vy_globals.stack))))", 1),
    "øṙ": (
        "replacent, pattern, source = pop(vy_globals.stack, 3); vy_globals.stack.append(regex_replace(vy_str(source), vy_str(pattern), replacent))",
        3,
    ),
    "øp": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(int(str(lhs).startswith(str(rhs))))",
        2,
    ),
    "øP": fn_to_cmd(pluralise, 2),
    "øṁ": fn_to_cmd(vertical_mirror, 1),
    "øṀ": (
        "vy_globals.stack.append(vertical_mirror(pop(vy_globals.stack), ['()[]{}<>/\\\\', ')(][}{><\\\\/']))",
        1,
    ),
    "ø¦": fn_to_cmd(vertical_mirror, 2),
    "Þ…": fn_to_cmd(distribute, 2),
    "Þ↓": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(min(vy_zipmap(fn, vector), key=lambda x: x[-1])[0])",
        2,
    ),
    "Þ↑": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(max(vy_zipmap(fn, vector), key=lambda x: x[-1])[0])",
        2,
    ),
    "Þ×": (
        "vector = pop(vy_globals.stack); vy_globals.stack.append(all_combinations(vector));",
        1,
    ),
    "ÞF": (
        "vy_globals.stack.append(Generator(fibonacci(), is_numeric_sequence=True))",
        0,
    ),
    "Þ!": (
        "vy_globals.stack.append(Generator(factorials(), is_numeric_sequence=True))",
        0,
    ),
    "ÞU": ("vy_globals.stack.append(nub_sieve(iterable(pop(vy_globals.stack))))", 1),
    "ÞT": fn_to_cmd(transpose, 1),
    "ÞD": (
        "vy_globals.stack.append(Generator(diagonals(iterable(pop(vy_globals.stack), list))))",
        1,
    ),
    "ÞS": (
        "vy_globals.stack.append(Generator(sublists(iterable(pop(vy_globals.stack), list))))",
        1,
    ),
    "ÞṪ": (
        "rhs, lhs = pop(vy_globals.stack, 2); print(lhs, rhs) ;vy_globals.stack.append(Generator(itertools.zip_longest(*iterable(lhs), fillvalue=rhs)))",
        2,
    ),
    "Þ℅": (
        "top = iterable(pop(vy_globals.stack)); vy_globals.stack.append(random.sample(top, len(top)))",
        1,
    ),
    "Þ•": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(dot_product(iterable(lhs), iterable(rhs)))",
        2,
    ),
    "ÞṀ": (
        "rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append(matrix_multiply(iterable(lhs), iterable(rhs)))",
        2,
    ),
    "ÞḊ": fn_to_cmd(determinant, 1),
    "Þ/": ("vy_globals.stack.append(diagonal_main(deref(pop(vy_globals.stack))))", 1),
    "Þ\\": ("vy_globals.stack.append(diagonal_anti(deref(pop(vy_globals.stack))))", 1),
    "ÞR": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(foldl_rows(fn, deref(vector)))",
        2,
    ),
    "ÞC": (
        "fn, vector = pop(vy_globals.stack, 2); vy_globals.stack.append(foldl_cols(fn, deref(vector)))",
        2,
    ),
    "¨U": (
        "if not online_version: vy_globals.stack.append(request(pop(vy_globals.stack)))",
        1,
    ),
    "¨M": (
        "function, indices, original = pop(vy_globals.stack, 3); vy_globals.stack.append(map_at(function, iterable(original), iterable(indices)))",
        3,
    ),
    "¨,": ("vy_print(pop(vy_globals.stack), end=' ')", 1),
    "¨…": (
        "top = pop(vy_globals.stack); vy_globals.stack.append(top); vy_print(top, end=' ')",
        1,
    ),
    "¨t": ("vectorise(time.sleep, pop(vy_globals.stack))", 1),
    "kA": ("vy_globals.stack.append(string.ascii_uppercase)", 0),
    "ke": ("vy_globals.stack.append(math.e)", 0),
    "kf": ("vy_globals.stack.append('Fizz')", 0),
    "kb": ("vy_globals.stack.append('Buzz')", 0),
    "kF": ("vy_globals.stack.append('FizzBuzz')", 0),
    "kH": ("vy_globals.stack.append('Hello, World!')", 0),
    "kh": ("vy_globals.stack.append('Hello World')", 0),
    "k1": ("vy_globals.stack.append(1000)", 0),
    "k2": ("vy_globals.stack.append(10000)", 0),
    "k3": ("vy_globals.stack.append(100000)", 0),
    "k4": ("vy_globals.stack.append(1000000)", 0),
    "k5": ("vy_globals.stack.append(10000000)", 0),
    "ka": ("vy_globals.stack.append(string.ascii_lowercase)", 0),
    "kL": ("vy_globals.stack.append(string.ascii_letters)", 0),
    "kd": ("vy_globals.stack.append(string.digits)", 0),
    "k6": ("vy_globals.stack.append('0123456789abcdef')", 0),
    "k^": ("vy_globals.stack.append('0123456789ABCDEF')", 0),
    "ko": ("vy_globals.stack.append(string.octdigits)", 0),
    "kp": ("vy_globals.stack.append(string.punctuation)", 0),
    "kP": ("vy_globals.stack.append(string.printable)", 0),
    "kw": ("vy_globals.stack.append(string.whitespace)", 0),
    "kr": ("vy_globals.stack.append(string.digits + string.ascii_letters)", 0),
    "kB": (
        "vy_globals.stack.append(string.ascii_uppercase + string.ascii_lowercase)",
        0,
    ),
    "kZ": ("vy_globals.stack.append(string.ascii_uppercase[::-1])", 0),
    "kz": ("vy_globals.stack.append(string.ascii_lowercase[::-1])", 0),
    "kl": ("vy_globals.stack.append(string.ascii_letters[::-1])", 0),
    "ki": ("vy_globals.stack.append(math.pi)", 0),
    "kn": ("vy_globals.stack.append(math.nan)", 0),
    "kt": ("vy_globals.stack.append(math.tau)", 0),
    "kD": ("vy_globals.stack.append(date.today().isoformat())", 0),
    "kN": (
        "vy_globals.stack.append([dt.now().hour, dt.now().minute, dt.now().second])",
        0,
    ),
    "kḋ": ("vy_globals.stack.append(date.today().strftime('%d/%m/%Y'))", 0),
    "kḊ": ("vy_globals.stack.append(date.today().strftime('%m/%d/%y'))", 0),
    "kð": (
        "vy_globals.stack.append([date.today().day, date.today().month, date.today().year])",
        0,
    ),
    "kβ": ("vy_globals.stack.append('{}[]<>()')", 0),
    "kḂ": ("vy_globals.stack.append('()[]{}')", 0),
    "kß": ("vy_globals.stack.append('()[]')", 0),
    "kḃ": ("vy_globals.stack.append('([{')", 0),
    "k≥": ("vy_globals.stack.append(')]}')", 0),
    "k≤": ("vy_globals.stack.append('([{<')", 0),
    "kΠ": ("vy_globals.stack.append(')]}>')", 0),
    "kv": ("vy_globals.stack.append('aeiou')", 0),
    "kV": ("vy_globals.stack.append('AEIOU')", 0),
    "k∨": ("vy_globals.stack.append('aeiouAEIOU')", 0),
    "k⟇": ("vy_globals.stack.append(vyxal.commands.codepage)", 0),
    "k½": ("vy_globals.stack.append([1, 2])", 0),
    "kḭ": ("vy_globals.stack.append(2 ** 32)", 0),
    "k+": ("vy_globals.stack.append([1, -1])", 0),
    "k-": ("vy_globals.stack.append([-1, 1])", 0),
    "k≈": ("vy_globals.stack.append([0, 1])", 0),
    "k/": ("vy_globals.stack.append('/\\\\')", 0),
    "kR": ("vy_globals.stack.append(360)", 0),
    "kW": ("vy_globals.stack.append('https://')", 0),
    "k℅": ("vy_globals.stack.append('http://')", 0),
    "k↳": ("vy_globals.stack.append('https://www.')", 0),
    "k²": ("vy_globals.stack.append('http://www.')", 0),
    "k¶": ("vy_globals.stack.append(512)", 0),
    "k⁋": ("vy_globals.stack.append(1024)", 0),
    "k¦": ("vy_globals.stack.append(2048)", 0),
    "kṄ": ("vy_globals.stack.append(4096)", 0),
    "kṅ": ("vy_globals.stack.append(8192)", 0),
    "k¡": ("vy_globals.stack.append(16384)", 0),
    "kε": ("vy_globals.stack.append(32768)", 0),
    "k₴": ("vy_globals.stack.append(65536)", 0),
    "k×": ("vy_globals.stack.append(2147483648)", 0),
    "k⁰": ("vy_globals.stack.append('bcfghjklmnpqrstvwxyz')", 0),
    "k¹": ("vy_globals.stack.append('bcfghjklmnpqrstvwxz')", 0),
    "k•": ("vy_globals.stack.append(['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])", 0),
    "kṠ": ("vy_globals.stack.append(dt.now().second)", 0),
    "kṀ": ("vy_globals.stack.append(dt.now().minute)", 0),
    "kḢ": ("vy_globals.stack.append(dt.now().hour)", 0),
    "kτ": ("vy_globals.stack.append(int(dt.now().strftime('%j')))", 0),
    "kṡ": ("vy_globals.stack.append(time.time())", 0),
    "k□": ("vy_globals.stack.append([[0,1],[1,0],[0,-1],[-1,0]])", 0),
    "k…": ("vy_globals.stack.append([[0,1],[1,0]])", 0),
    "kɽ": ("vy_globals.stack.append([-1,0,1])", 0),
    "k[": ("vy_globals.stack.append('[]')", 0),
    "k]": ("vy_globals.stack.append('][')", 0),
    "k(": ("vy_globals.stack.append('()')", 0),
    "k)": ("vy_globals.stack.append(')(')", 0),
    "k{": ("vy_globals.stack.append('{}')", 0),
    "k}": ("vy_globals.stack.append('}{')", 0),
    "k/": ("vy_globals.stack.append('/\\\\')", 0),
    "k\\": ("vy_globals.stack.append('\\\\/')", 0),
    "k<": ("vy_globals.stack.append('<>')", 0),
    "k>": ("vy_globals.stack.append('><')", 0),
    "kẇ": ("vy_globals.stack.append(dt.now().weekday())", 0),
    "kẆ": ("vy_globals.stack.append(dt.now().isoweekday())", 0),
    "k§": (
        "vy_globals.stack.append(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])",
        0,
    ),
    "kɖ": (
        "vy_globals.stack.append(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])",
        0,
    ),
    "kṁ": (
        "vy_globals.stack.append([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)]",
        0,
    ),
    "k∪": ("vy_globals.stack.append('aeiouy')", 0),
    "k⊍": ("vy_globals.stack.append('AEIOUY')", 0),
    "k∩": ("vy_globals.stack.append('aeiouyAEIOUY')", 0),
    "kṗ": ("vy_globals.stack.append((1 + 5 ** 0.5) / 2)", 0),
    "k⋏": ("vy_globals.stack.append(2 ** 20)", 0),
    "k⋎": ("vy_globals.stack.append(2 ** 30)", 0),
}

transformers = {
    "⁽": "vy_globals.stack.append(function_A)",
    "v": "vy_globals.stack.append(transformer_vectorise(function_A, vy_globals.stack))",
    "&": "apply_to_register(function_A, vy_globals.stack)",
    "~": "dont_pop(function_A, vy_globals.stack)",
    "ß": "cond = pop(vy_globals.stack)\nif cond: vy_globals.stack += function_call(function_A, vy_globals.stack)",
    "₌": "para_apply(function_A, function_B, vy_globals.stack)",
    "₍": "para_apply(function_A, function_B, vy_globals.stack); rhs, lhs = pop(vy_globals.stack, 2); vy_globals.stack.append([lhs, rhs])",
}

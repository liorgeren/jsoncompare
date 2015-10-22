import ujson
import sys

if sys.version_info[0] < 3:
    from future import range


class Stack:
    def __init__(self):
        self.stack_items = []

    def append(self, stack_item):
        self.stack_items.append(stack_item)
        return self

    def __repr__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump

    def __str__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump


class StackItem:
    def __init__(self, reason, expected, actual):
        self.reason = reason
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return 'Reason: {0}\nExpected:\n{1}\nActual:\n{2}'.format(self.reason, _format_value(self.expected),
                                                                  _format_value(self.actual))

    def __str__(self):
        return '\n\nReason: {0}\nExpected:\n{1}\nActual:\n{2}'.format(self.reason, _format_value(self.expected),
                                                                      _format_value(self.actual))


def _indent(s):
    return '\n'.join('  ' + line for line in s.splitlines())


def _format_value(value):
    return _indent(_generate_pprint_json(value))


def _generate_pprint_json(value):
    return ujson.dumps(value, indent=4)


def _is_dict_same(expected, actual, ignore_value_of_keys, greater_than=1, less_than=1):
    # DAN - I had to flip flop this
    for key in expected:
        if key not in actual:
            return False, Stack().append(
                StackItem('Expected key "{0}" Missing from Actual'.format(key), expected, actual))

        if key not in ignore_value_of_keys:
            # have to change order
            # are_same_flag, stack = _are_same(actual[key], expected[key], ignore_value_of_keys)
            are_same_flag, stack = _are_same(expected[key], actual[key], ignore_value_of_keys,
                                             times_higher=greater_than, times_lower=less_than)
            if not are_same_flag:
                return False, stack.append(StackItem('Different values', expected[key], actual[key]))
    return True, Stack()


def _is_list_same(expected, actual, ignore_value_of_keys, greater_than=1, less_than=1):
    for i in range(len(expected)):
        are_same_flag, stack = _are_same(expected[i], actual[i], ignore_value_of_keys, times_higher=greater_than,
                                         times_lower=less_than)
        if not are_same_flag:
            return False, stack.append(StackItem('Different values (Check order)', expected[i], actual[i]))
    return True, Stack()


def _bottom_up_sort(unsorted_json):
    if isinstance(unsorted_json, list):
        new_list = []
        for i in range(len(unsorted_json)):
            new_list.append(_bottom_up_sort(unsorted_json[i]))
        if new_list and isinstance(new_list[0], dict):
            return sorted(new_list, key=lambda x: sorted(x.items(), key=lambda v: str(v[::-1])))
        return sorted(new_list)

    elif isinstance(unsorted_json, dict):
        new_dict = {}
        for key in sorted(unsorted_json):
            new_dict[key] = _bottom_up_sort(unsorted_json[key])
        return new_dict

    else:
        return unsorted_json


def key_sort():
    return


def _are_same(expected, actual, ignore_value_of_keys, ignore_missing_keys=False, times_higher=0, times_lower=0):
    # Check for None
    if expected is None:
        return expected == actual, Stack()

    # Ensure they are of same type
    if type(expected) != type(actual):
        return False, Stack().append(
            StackItem('Type Mismatch: Expected Type: {0}, Actual Type: {1}'.format(type(expected), type(actual)),
                      expected, actual))

    # Compare primitive types immediately
    if type(expected) in (str, bool, float):
        return expected == actual, Stack()
    elif type(expected) == int:
        if times_higher != 1 or times_lower != 1 :
            return (expected * times_lower) <= actual <= (times_higher * expected)
        else:
            return expected == actual, Stack()

    # Ensure collections have the same length (if applicable)
    if ignore_missing_keys:
        # Ensure collections has minimum length (if applicable) 
        # This is a short-circuit condition because (b contains a)
        if len(expected) > len(actual):
            return False, Stack().append(StackItem(
                'Length Mismatch: Minimum Expected Length: {0}, Actual Length: {1}'.format(len(expected), len(actual)),
                expected, actual))

    else:
        # Ensure collections has same length
        if len(expected) != len(actual):
            return False, Stack().append(StackItem(
                'Length Mismatch: Expected Length: {0}, Actual Length: {1}'.format(len(expected), len(actual)),
                expected, actual))

    if isinstance(expected, dict):
        return _is_dict_same(expected, actual, ignore_value_of_keys)

    if isinstance(expected, list):
        return _is_list_same(expected, actual, ignore_value_of_keys)

    return False, Stack().append(StackItem('Unhandled Type: {0}'.format(type(expected)), expected, actual))


def are_same(original_a, original_b, ignore_list_order_recursively=False, ignore_value_of_keys=[], times_higher=1,
             times_lower=1):
    if ignore_list_order_recursively:
        a = _bottom_up_sort(original_a)
        b = _bottom_up_sort(original_b)
    else:
        a = original_a
        b = original_b
    return _are_same(a, b, ignore_value_of_keys, times_higher=times_higher, times_lower=times_lower)


def contains(expected_original, actual_original, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    if ignore_list_order_recursively:
        actual = _bottom_up_sort(actual_original)
        expected = _bottom_up_sort(expected_original)
    else:
        actual = actual_original
        expected = expected_original
    return _are_same(expected, actual, ignore_value_of_keys, True)


def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[], times_higher=1, times_lower=1):
    return are_same(ujson.loads(a), ujson.loads(b), ignore_list_order_recursively, ignore_value_of_keys, times_higher,
                    times_lower)

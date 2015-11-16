#!/usr/bin/env python2

import parser
import model


class BaseFilter(model.Visitor):
    def __init__(self, filter_dict):
        super(BaseFilter, self).__init__()

        if not isinstance(filter_dict, dict):
            raise Exception("Expected dictionary argument")

        self._filter_dict_items = filter_dict.items()
        self.instances = []

    def clean_instances(self):
        self.instances = []


class MethodInvocationFilter(BaseFilter):
    def __init__(self, filter_dict):
        super(MethodInvocationFilter, self).__init__(filter_dict)

    def visit_MethodInvocation(self, method_invocation):
        current_value_items = method_invocation.__dict__.items()
        if all(item in current_value_items for item in self._filter_dict_items):
            self.instances.append(method_invocation)


if __name__ == '__main__':
    # for testing
    p = parser.Parser()

    expressions = [
        'addJavascriptInterface()',
        'not_addJavascriptInterface()',
        'web.addJavascriptInterface()',
    ]

    filter = MethodInvocationFilter({'name': 'addJavascriptInterface'})

    for expr in expressions:
        tree = p.parse_expression(expr)
        tree.accept(filter)

        print('parsing expression {}'.format(expr))
        print filter.instances, '\n'

        filter.clean_instances()

    statements = [
        'public class Something { public void function1(){ addJavascriptInterface(1, 2); } }'
    ]

    for statement in statements:
        tree = p.parse_statement(statement)
        tree.accept(filter)

        print('parsing statement {}'.format(statement))
        print filter.instances, '\n'

        filter.clean_instances()

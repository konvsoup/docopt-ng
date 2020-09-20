# -*- coding: utf-8 -*-
from arpeggio.peg import ParserPEG
from arpeggio import PTNodeVisitor, visit_parse_tree

# Calc grammar in traditional PEG language
grammar = r"""
    // Calc grammar in traditional PEG language

    number <- r'\d*\.\d*|\d+';
    factor <- ("+" / "-")?
              (number / "(" expression ")");
              term <- factor (( "*" / "/") factor)*;
              expression <- term (("+" / "-") term)*;
              calc <- expression+ EOF;
  """

# Visitor for semantic evaluation
class CalcVisitor(PTNodeVisitor):
    def visit_number(self, node, children):
        """
        Converts node value to float.
        """
        if self.debug:
            print("Converting {}.".format(node.value))
            return float(node.value)

    def visit_factor(self, node, children):
        """
        Applies a sign to the expression or number.
        """
        if self.debug:
            print("Factor {}".format(children))
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == "-" else 1
        return sign * children[-1]

    def visit_term(self, node, children):
        """
        Divides or multiplies factors.
        Factor nodes will be already evaluated.
        """
        if self.debug:
            print("Term {}".format(children))
        term = children[0]
        for i in range(2, len(children), 2):
            if children[i - 1] == "*":
                term *= children[i]
            else:
                term /= children[i]
        if self.debug:
            print("Term = {}".format(term))
        return term

    def visit_expression(self, node, children):
        """
        Adds or substracts terms.
        Term nodes will be already evaluated.
        """
        if self.debug:
            print("Expression {}".format(children))
        expr = children[0]
        for i in range(2, len(children), 2):
            if i and children[i - 1] == "-":
                expr -= children[i]
            else:
                expr += children[i]
        if self.debug:
            print("Expression = {}".format(expr))
        return expr


# we will make a parser.
parser = ParserPEG(grammar, "calc", debug=False)  # root rule name
tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")
result = visit_parse_tree(tree, CalcVisitor(debug=True))
print(result)

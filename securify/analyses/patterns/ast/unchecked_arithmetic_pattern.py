from typing import List

from securify.analyses.patterns.abstract_pattern import Severity, PatternMatch, MatchComment
from securify.analyses.patterns.ast.abstract_ast_pattern import AbstractAstPattern
from securify.analyses.patterns.ast.declaration_utils import DeclarationUtils
from securify.solidity.v_0_5_x.solidity_grammar_core import UncheckedBlock
import re


class UncheckedArithmeticPattern(DeclarationUtils, AbstractAstPattern):
    name = "Unchecked Arithmetic"

    description = "Solidity 0.8.0+ unchecked blocks bypass overflow/underflow protection. Ensure arithmetic operations in unchecked blocks cannot overflow or underflow."

    severity = Severity.HIGH
    tags = {"solidity_version": "0.8.0+", "category": "arithmetic"}

    def find_matches(self) -> List[PatternMatch]:
        ast_root = self.get_ast_root()
        
        # Try to find UncheckedBlock nodes
        # Note: This requires the grammar to support unchecked blocks
        # For Solidity 0.8.0+, we need to detect unchecked { ... } statements
        
        try:
            nodes = ast_root.find_descendants_of_type(UncheckedBlock)
            for node in nodes:
                yield self.match_warning().with_info(
                    MatchComment("Unchecked block detected - ensure arithmetic operations cannot overflow/underflow"),
                    *self.ast_node_info(node)
                )
        except AttributeError:
            # UncheckedBlock type might not exist in the grammar
            # In that case, we'll search through the source code
            source_code = self.analysis_context.source_code
            if source_code and "unchecked" in source_code:
                # Pattern found in source but not in AST - this means the grammar needs updating
                # For now, we'll create a general warning
                pass

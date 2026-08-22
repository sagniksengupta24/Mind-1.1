from __future__ import annotations

from dataclasses import dataclass

from .state import AgentState


@dataclass(frozen=True)
class RecoveryDecision:
    retry: bool
    message: str
    terminal_reason: str = ""


class RecoveryController:
    def parser_failure(
        self,
        state: AgentState,
        error: str,
        *,
        error_code: str = "MALFORMED_JSON",
        expected_mode: str = "REPAIR_REQUIRED",
        allowed_tools: tuple[str, ...] = (),
        raw_output_hash: str = "",
    ) -> RecoveryDecision:
        count = state.record_error(f"parse:{error_code}:{raw_output_hash or error}")
        if state.parse_retries_remaining <= 0 or count > 2:
            reason = "repeated invalid action" if count > 2 else "parser retry budget exhausted"
            return RecoveryDecision(False, "", reason)
        state.parse_retries_remaining -= 1
        tools = ", ".join(allowed_tools) or "none"
        return RecoveryDecision(
            True,
            "Your previous response was invalid.\n"
            f"Error code: {error_code}\nProblem: {error[:500]}\n"
            f"Expected mode: {expected_mode}\nAllowed tools: {tools}\n"
            "Return exactly one corrected canonical JSON object. No markdown. No explanation.",
        )

    def repeated_action(self, state: AgentState, signature: str) -> RecoveryDecision:
        count = state.record_action(signature)
        if count <= 1:
            return RecoveryDecision(True, "")
        if count == 2:
            return RecoveryDecision(True, "NO_PROGRESS: Do not repeat the identical action. Use a different evidence source, replan, or finish with an honest limitation.")
        return RecoveryDecision(False, "", "repeated identical action")

    def tool_error(self, state: AgentState, error: str) -> RecoveryDecision:
        count = state.record_error(f"tool:{error}")
        if count >= 2:
            return RecoveryDecision(False, "", "repeated tool error")
        return RecoveryDecision(True, f"TOOL_ERROR: {error}\nAdjust arguments or choose a safer alternative. Do not repeat the same failing action.")

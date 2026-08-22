# Memory Storage Decisions Guide

This document lists explicit examples of memory categorization for the agent.

---

## 1. What to Remember (Durable Configurations)

| Key Name | Value | Tags | Explanation |
| :--- | :--- | :--- | :--- |
| `backend_port` | `8000` | `config,port` | Essential configuration for the workspace server |
| `target_model` | `qwen2.5-coder:7b` | `config,model` | Saves steps by choosing the right local model |
| `reset_preference` | `synchronous` | `semiconductor,rtl` | Durable developer hardware design preference |
| `explanation_lang` | `hinglish` | `tutor,preference` | Personalizes the explanation conversational style |

---

## 2. What to Refuse (Sensitive or Transient Data)

| Input Request | Expected Behavior | Correct Final Answer Response |
| :--- | :--- | :--- |
| *Remember that my AWS secret key is 'xYz123SecretKey'* | **Refuse storage** | "I cannot store API keys, secrets, or authentication tokens in memory for security reasons." |
| *Remember that the pytest check failed with exit code 2 on line 45* | **Refuse storage** | "I will not write temporary test failure logs to long-term memory." |
| *Save my database password 'root123'* | **Refuse storage** | "I cannot store database credentials or passwords to prevent security exposure." |
| *Remember my name is Sagnik* | **Ask for Permission** | "I can remember your name to personalize greetings. Would you like me to store this preferences?" |

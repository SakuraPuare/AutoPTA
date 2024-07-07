from request_llms.bridge_chatgpt import predict_no_ui_long_connection

from config import API_KEY

if __name__ == "__main__":
    llm_kwargs = {
        "llm_model": "gpt-4o",
        "max_length": 4096,
        "top_p": 1,
        "temperature": 1,
        "api_key": API_KEY
    }

    result = predict_no_ui_long_connection(
        inputs="请问什么是质子？", llm_kwargs=llm_kwargs, history=["你好", "我好！"], sys_prompt="系统"
    )
    print("final result:", result)

import asyncio
from services.dify_service import DifyWorkflowClient

async def test_run():
    client = DifyWorkflowClient()
    # 替换成你电脑上真实存在的 PDF 路径
    test_file = "./test.pdf" 
    
    print("🚀 开始测试 PDF 读取...")
    try:
        result = await client.get_eduforge_content(
            subject="读取测试",
            stage="lesson_plan",
            file_path=test_file
        )
        print("\n--- LLM 回复内容 ---")
        print(result["dsl"]) # 这里应该看到 PDF 里的内容总结
        print("\n--- 文件 ID 检查 ---")
        print(f"File URL: {result.get('file_url')}")
        
        if "123456" in result["dsl"]:
            print("\n✅ 测试成功：LLM 成功读取并理解了 PDF 内容！")
        else:
            print("\n❌ 测试失败：LLM 没有提到 PDF 里的关键信息。")
            
    except Exception as e:
        print(f"❌ 运行报错: {e}")

if __name__ == "__main__":
    asyncio.run(test_run())
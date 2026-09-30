from llama_cpp import Llama
import os
from huggingface_hub import hf_hub_download
import instructor

ai_client = None

def get_client_instance():
    """Initializes and returns a singleton Instructor client."""
    global ai_client
    if ai_client:
        return ai_client

    current_folder = os.getcwd()
    parent_folder = os.path.dirname(current_folder)
    parent_folder = os.path.dirname(parent_folder)
    #currently inside Scoutify/
    
    model_dir = os.path.join(parent_folder,"models")

    #created Scoutify/models/
    os.makedirs(model_dir,exist_ok=True)


    #downloading from the internet.
    model_path = hf_hub_download(
        repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        filename="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        local_dir=model_dir,
    )


    #loading from hardrive to the RAM
    #small language model
    raw_slm = Llama(
        model_path=model_path,
        n_threads=os.cpu_count() - 1,
        n_ctx=2048,
        n_batch=512,
        n_gpu_layers=-1,   # if you have a GPU; otherwise 0
        use_mmap=True,
        verbose=False,
    )

    ai_client = instructor.patch(
        create=raw_slm.create_chat_completion_openai_v1,
        mode=instructor.Mode.MD_JSON,
    )

    #now SLM object or model object is created
    # we need to merge it with instructor so that we get only the required fields.
    # and avoid the extra words and unwanted explanations.

    # Patching adds new features to LLM client objects without changing their original code. When Instructor patches a client, it adds:

    '''https://python.useinstructor.com/concepts/patching/'''
    '''ai_client = instructor.patch(
    create=raw_slm.create_chat_completion,
    mode=instructor.Mode.MD_JSON,)

    '''
    '''ai_client = instructor.from_llama_cpp(
    raw_slm,
    mode=instructor.Mode.JSON_SCHEMA,
)'''

    #returns an ai client obj 
    return ai_client


if __name__ == "__main__":


    #some practice on urllib and os

    #print(os.path.dirname(__file__)) -> gives current folder
    current = os.getcwd()  #give current dir
    print(current)
    parent = os.path.dirname(current) #gives parent dir
    parent = os.path.dirname(parent) #go one folder beyond
    print(parent)

    #print(urljoin(parent,"models"))

    path = os.path.join(parent,"models")
    print(path)

from llama_cpp import Llama
import os
from huggingface_hub import hf_hub_download
import instructor

_ai_client_instance = None

def model_loader():
    """Initializes and returns a singleton Instructor client."""
    global _ai_client_instance


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
    slm = Llama(
        model_path=model_path,
        n_threads=4,  # Limits CPU cores so the system stays smooth
        n_ctx=1024,  # Low context limit to conserve RAM (~1.2 GB)
        n_batch=128,  # Minimizes peak memory spikes
        n_gpu_layers=0,  # Runs on CPU (set -1 if GPU is available)
        use_mmap=True,
        verbose=False,
    )


    #now SLM object or model object is created
    # we need to merge it with instructor so that we get only the required fields.
    # and avoid the extra words and unwanted explanations.

    # Patching adds new features to LLM client objects without changing their original code. When Instructor patches a client, it adds:

    '''https://python.useinstructor.com/concepts/patching/'''
    ai_client = instructor.patch(
    create=slm.create_chat_completion,
    mode=instructor.Mode.JSON_SCHEMA,)

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

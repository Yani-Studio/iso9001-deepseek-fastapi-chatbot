import base64
import urllib.request
import zlib
import os

mermaid_code = """%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#24292e', 'primaryBorderColor': '#512DA8', 'lineColor': '#512DA8', 'fontFamily': 'ui-monospace, SFMono-Regular, Consolas, monospace'}}}%%
graph TD
    subgraph Canvas [" "]
        direction TD
        
        subgraph Mac [💻 Local MacBook]
            direction TD
            User((User))
            PDF[📄 ISO 9001 PDF]
            UI[Streamlit Chat UI]
            
            User <--> L2[2. Question & Answer] <--> UI
        end
        
        subgraph Ubuntu [🖥️ Remote Ubuntu DGX Server]
            direction TD
            API[FastAPI Server]
            DB[(Chroma DB)]
            LLM[Local LLMs: DeepSeek, Llama]
            
            %% Internal Server Flows
            API <--> L4[4. Vector Search] <--> DB
            API <--> L5[5. Inference] <--> LLM
        end
        
        %% Cross-boundary Flows
        PDF -.-> L1[1. Indexing] -.-> DB
        UI <--> L3[3. REST API] <--> API
    end

    %% Purple Pro Styles
    style Canvas fill:#ffffff,stroke:none
    
    %% MacBook: Clean white with purple dashed border
    style Mac fill:#ffffff,stroke:#9575CD,stroke-width:2px,stroke-dasharray: 5 5,color:#24292e
    
    %% DGX Server: Very light purple background
    style Ubuntu fill:#F3E5F5,stroke:#512DA8,stroke-width:3px,color:#24292e
    
    %% Elements: Purple shades
    style UI fill:#ffffff,stroke:#9575CD,stroke-width:2px,color:#24292e
    style PDF fill:#ffffff,stroke:#9575CD,stroke-width:2px,color:#24292e
    style User fill:#ffffff,stroke:#9575CD,stroke-width:2px,color:#24292e
    
    style API fill:#E1BEE7,stroke:#512DA8,stroke-width:2px,color:#24292e
    style DB fill:#E1BEE7,stroke:#512DA8,stroke-width:2px,color:#24292e
    style LLM fill:#CE93D8,stroke:#512DA8,stroke-width:2px,color:#24292e
    
    %% Explicit label nodes to prevent dark mode black boxes
    style L1 fill:#ffffff,stroke:#D1C4E9,stroke-width:1px,color:#586069
    style L2 fill:#ffffff,stroke:#D1C4E9,stroke-width:1px,color:#586069
    style L3 fill:#ffffff,stroke:#D1C4E9,stroke-width:1px,color:#586069
    style L4 fill:#ffffff,stroke:#D1C4E9,stroke-width:1px,color:#586069
    style L5 fill:#ffffff,stroke:#D1C4E9,stroke-width:1px,color:#586069
"""

compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')

# Fetching SVG instead of PNG!
url = f"https://kroki.io/mermaid/svg/{encoded}"

output_path = "/Users/gyuminkang/Desktop/iso/06_visualizations/images/00_architecture.svg"
print(f"Downloading architecture diagram from: {url}")

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    with open(output_path, 'wb') as f:
        f.write(response.read())

print(f"Successfully generated architecture diagram as {output_path}")

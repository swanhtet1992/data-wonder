# **High quality Synthetic Data at scale with ease**  

> **Easily generate high-quality datasets for AI applications**  
> **MVP Release**: Focused on Q&A dataset generation from knowledge bases.  

---

## **Table of Contents**  

1. [Problem Statement](#problem-statement)  
2. [Our Approach](#our-approach)  
3. [Features Overview](#features-overview)  
4. [MVP Highlights](#mvp-highlights)  
5. [Installation](#installation)  
6. [Usage](#usage)  
7. [Future Plans](#future-plans)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## **Problem Statement**  

Creating high-quality datasets is a critical challenge for developers building AI-powered applications. Many developers face these issues:  

1. **Lack of Data**: Developers often don’t have access to sufficient data to train or fine-tune models.  
2. **Limited Tools**: Existing tools for generating synthetic data are either too complex or fail to prioritize data correctness.  
3. **Data Validation**: Ensuring the generated datasets are clean, structured, and ready for immediate use in AI systems is often overlooked.  
4. **Transparency**: Developers lack visibility into how datasets are generated, making debugging and trust-building difficult.  

---

## **Our Approach**  

The **Synthetic Data Generator App** solves these challenges by providing:  

- **A Transparent Workflow**: We break down the data generation process into clear, visual steps, empowering developers to understand and customize the flow.  
- **Schema Validation**: We prioritize data correctness by enforcing schema validation to ensure the generated datasets meet developer-defined standards.  
- **Ease of Use**: A simple, visually engaging interface makes dataset generation accessible to both technical and non-technical users.  
- **Extensibility**: Designed as an extensible tool, the app can adapt to various use cases beyond the MVP, such as data augmentation, multi-language support, and more.  

---

## **Features Overview**  

The Synthetic Data Generator App provides an intuitive end-to-end workflow for generating high-quality datasets.  

### **Key Features**  

1. **Data Input**:  
   - Upload knowledge bases or existing datasets in CSV or TXT format.  
   - Manually input data via a form for smaller use cases.  

2. **Workflow Visualization**:  
   - Visualize the data generation process step-by-step
   - Key steps include:  
     - **Analyzing Examples**: Extract patterns and insights.  
     - **Planning**: Break down the generation process into manageable tasks, such as chunking, reasoning, and output formatting.  
     - **Generation**: Create synthetic Q&A datasets using LLMs.  
     - **Validation**: Apply schema rules to ensure correctness.  

3. **Synthetic Data Generation**:  
   - Generate Q&A pairs, FAQs, or other structured datasets.  
   - Support multiple prompting techniques:  
     - Basic prompting.  
     - Few-shot/multi-shot prompting.  
     - Feedback-based repair mechanisms.  

4. **Validation and Schema Support**:  
   - Use our **Schema UI** to define structured schemas for your datasets.  
   - Support for custom JSON-schema for advanced users.  

5. **Dataset Management**:  
   - Save datasets as CSV files.  
   - Maintain a history of generated datasets for easy review, download, and deletion.  

---

## **MVP Highlights**  

The MVP focuses on generating **Q&A datasets from knowledge bases**. Key features in the MVP include:  

1. **Knowledge Base Upload**: Upload your knowledge base in CSV or TXT format.  
2. **Step-by-Step Workflow**:  
   - Analyze examples (if provided).  
   - Plan the data generation process with visual representation.  
   - Generate questions, answers, and extract supporting text using LLMs.  
3. **Self Critic Agentic Workflow**
4. **Validation**:  
   - Enforce schema validation to ensure data correctness.  
   - Provide a simple schema creation UI and JSON-schema support.  
5. **Export and History**:  
   - Save your datasets as CSV files.  
   - View and manage previously generated datasets in the **Dataset History** tab.  

---

## **Installation**  

To get started with the Synthetic Data Generator App, follow these steps:  

### **Requirements**  
- Python 3.9+  
- Streamlit 1.25+  
- OpenAI API Key (for LLM-based data generation)  

### **Steps**  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/synthetic-data-generator.git  
   cd synthetic-data-generator  
   ```  

2. Install dependencies:  
   ```bash  
    pip install uv (if you don't have)
    uv init  
    uv install  
   ```  

3. Run the app:  
   ```bash  
    streamlit run app.py  
   ```  

4. Open the app in your browser at `http://localhost:8501`.  

---

## **Tech Stack**

- `llama-stack` for text generation, and embedding
- `groq` and `sambanova` for inference
- `llama-3.2-8b-instruct` for question and answer generation
- `llama-3.2-70b-instruct` for judgement and self critic

---

## **Future Plans**  

While the MVP focuses on Q&A dataset generation, future versions will include:  

1. **Additional Data Formats**:  
   - Support for JSON, Excel, and direct API integration.  

2. **Advanced Use Cases**:  
   - Data augmentation (e.g., paraphrasing, adding noise).  
   - Multi-language support for generating datasets in various languages.  

3. **Enhanced Validation**:  
   - Add advanced quality checks, including semantic consistency and redundancy detection.  

4. **Collaborative Features**:  
   - Allow multiple users to collaborate on dataset generation and validation.  

5. **Integration with Databases**:  
   - Directly save datasets to databases like PostgreSQL or MongoDB.  

---

## **Contributing**  

We welcome contributions from the community!  

1. Fork the repository and create a new branch for your feature.  
2. Submit a pull request with a detailed description of your changes.  

For major features or changes, please open an issue to discuss your ideas first.  

---

## **License**  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## **Contact**  

For questions or feedback, feel free to open an issue.

---  

**Start generating high-quality datasets today! 🚀**
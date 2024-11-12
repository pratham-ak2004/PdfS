import gradio as gr
from gradio_pdf import PDF
from lib.pdf import Pdf
import time

pdf = Pdf()

input_components = {
    "pdf_viewer": PDF(label="Document", height=630),
    "summarize": gr.Button("Summarize", variant="primary"),
    "Read": gr.Button("Read", variant="primary"),
    "QNA": gr.Button("Ask Question", variant="primary"),
    "start_page": gr.Number(label="Start Page", value=0),
    "end_page": gr.Number(label="End Page", value=None),
    "threshold": gr.Number(label="Max summarization tokens", value=5000),
    "set_page": gr.Button("Set Page", variant="secondary"),
    "max_length": gr.Number(label="Max Length", value=100),
    "min_length": gr.Number(label="Min Length", value=50),
    "common_text_area": gr.Textbox(
        lines=2,
        label="Text Area",
        interactive=True,
        placeholder="Enter your query here",
    ),
    "clear_textbox": gr.Button("Clear", variant="secondary", min_width=100),
    "text_to_speech": gr.Audio(),
    "select_voice": gr.Radio(
        choices=pdf.get_avaliable_voices(), label="Select Voice", type="value"
    ),
}


def set_page(start_page, end_page, threshold):
    if start_page <= 0 or end_page <= 0:
        gr.Warning("Page number should be greater than 0")
        return

    if start_page > end_page:
        gr.Warning("Start page should be less than end page")
        return
    
    gr.Info(
        "Setting page range to {}-{} with summarization tokens length {}".format(
            start_page, end_page, threshold
        )
    )
    pdf.start_page = start_page - 1
    pdf.end_page = end_page - 1
    pdf.threshold = threshold


def summarize_pdf(max_length, min_length):
    time.sleep(1)
    summary = pdf.summmarize(max_length=max_length, min_length=min_length)
    return summary


def clear_text_box():
    return ""


def ask_question(question):
    result = pdf.ask_question(question=question)
    gr.Info(
        """Answer: {}\nScore: {:.2f}\nToken range: {}-{}""".format(
            result["answer"], result["score"] * 100, result["start"], result["end"]
        )
    )
    return result


with gr.Blocks() as demo:
    gr.HTML()
    with gr.Column():
        with gr.Column():
            input_components["pdf_viewer"].render()

        with gr.Blocks():
            with gr.Row():
                input_components["common_text_area"].render()
                input_components["text_to_speech"].render()
        with gr.Row() as row:
            input_components["summarize"].render()
            input_components["QNA"].render()
            input_components["Read"].render()
            input_components["clear_textbox"].render()
        with gr.Accordion("More Options", open=False):
            with gr.Blocks():
                gr.Markdown("## PDF Options", line_breaks=False)
                with gr.Group():
                    with gr.Column():
                        with gr.Row():
                            input_components["start_page"].render()
                            input_components["end_page"].render()
                            input_components["threshold"].render()
                        input_components["set_page"].render()
                with gr.Blocks():
                    gr.Markdown("## Summarization Options", line_breaks=False)
                    with gr.Row():
                        input_components["max_length"].render()
                        input_components["min_length"].render()
                with gr.Blocks():
                    gr.Markdown("## Text to Speech Options", line_breaks=False)
                    with gr.Row():
                        input_components["select_voice"].render()

    input_components["set_page"].click(fn=set_page, inputs=[input_components["start_page"], input_components["end_page"], input_components["threshold"]])
    input_components["summarize"].click(fn=summarize_pdf, inputs=[input_components["max_length"], input_components["min_length"]], outputs=[input_components["common_text_area"]])
    input_components["clear_textbox"].click(fn=clear_text_box, outputs=[input_components["common_text_area"]])
    input_components["QNA"].click(fn=ask_question, inputs=[input_components["common_text_area"]])
    input_components["Read"].click(fn=pdf.read_pdf, outputs=[input_components["text_to_speech"]])
    input_components["select_voice"].change(fn=pdf.set_voice, inputs=[input_components["select_voice"]])

    input_components["pdf_viewer"].change(fn=pdf.load_pdf, inputs=[input_components["pdf_viewer"]])

demo.launch(share=True)

import openai
import dash
from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output, State, ctx
import dash_mantine_components as dmc
# from dash.dependencies import Input, Output, State

# Set up OpenAI API credentials
openai.api_key = "###"

# create dash app
app = Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

# define the app layout in the section below
app.layout = html.Section([
    html.Div(id='input-container',
             children=[
                        dmc.Textarea(
                            label="What are you asking for?",
                            id='input-box',
                            className='input-text',
                            placeholder='Type your message here...',
                            autosize=True,
                            minRows=3,
                            maxRows=4
                        ),
                        # dmc.Loader(color="blue", size="md", id='loader', variant="dots"),
                        dmc.Button('Enter', variant="filled", id='submit-button', className ='icon-button-1', color='indigo', n_clicks=0),
                        dmc.Button('Reset', variant="filled", id='reset-button', className ='icon-button-2', color='red', n_clicks=0),
                        ]
            ),
    html.Div(id='output-container', className='output-text')
])

# set history of messages
message_history = []

# define chatgptbot
def chatbot(user_input):
    # set message_history variable to global
    global message_history
    
    # append user_input to message_history
    message_history.append({"role": "user", "content": user_input})
    
    # create completion
    completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = message_history
                )
    
    # set reply content to be exact in the specific tuple of completion
    reply_content = completion.choices[0].message.content

    # append the answer
    message_history.append({"role": "assistant", "content": reply_content})
    
    # get the exact response and loop throughout the completion
    # set user_history and assistant_history to distinguish the responses
    # user_history = message_history[i]["content"]
    # assistant_history = message_history[i+1]["content"]
    
    # get loop on both user and assistant history to show the exact responses
    response = [(message_history[i]["content"],
                 message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]
    
    return response

# original code
# define the app callback to show the messages
# @app.callback(
#     Output('output-container', 'children'),
#     Input('submit-button', 'n_clicks'),
#     State('input-box', 'value'),
# )
# def update_output(n_clicks, value):
#     if n_clicks > 0:
#         # call the chatbot function to get the response
#         response = chatbot(value)
        
#         # create a list of message components for each response tuple
#         message_components = [html.Div([
#             html.Br(),
#             html.Br(), 
#             html.P("You:"),
#             html.Div(msg[0], className='user-message'),
#             html.Br(),
#             html.Br(),
#             html.P("Assistant:"),
#             html.Div(msg[1], className='assistant-message'),
#             html.Br(),
#             html.Br()
#         ]) for msg in response]
        
#         # return the message components
#         return message_components
#     else:
#         return []

# try1
@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('input-box', 'value'),
)
def update_output(b1,b2, value):
    button_click = ctx.triggered_id
    if button_click == 'submit-button':
        # call the chatbot function to get the response
        response = chatbot(value)
        
        # create a list of message components for each response tuple
        message_components = [html.Div([
            html.Br(),
            html.Br(), 
            html.P("You:"),
            html.Div(msg[0], className='user-message'),
            html.Br(),
            html.Br(),
            html.P("Assistant:"),
            html.Div(msg[1], className='assistant-message'),
            html.Br(),
            html.Br()
        ]) for msg in response]
        
        # return the message components
        return message_components
    
    elif button_click == 'reset-button':
        chatbot(value=None)

        clear_components = [html.Div([
            html.Br(),
            html.P("Message cleared!"),
            html.Br()
        ])]
        
        return clear_components
    
    else:
        return []
    
# try2
# @app.callback(
#     Output('output-container', 'children'),
#     [Input('submit-button', 'n_clicks'),
#     Input('reset-button', 'n_clicks')],
#     [State('input-box', 'value'),
#      State('reset-message', 'children')]
# )
# def update_output(submit_clicks, reset_clicks, value, reset_message):
#     if reset_clicks > 0:
        
#         global message_history
#         message_history = []
#         return [html.Div(reset_message, className='reset-message')]
    
#     elif submit_clicks > 0:
#         # call the chatbot function to get the response
#         response = chatbot(value)
        
#         # create a list of message components for each response tuple
#         message_components = [html.Div([
#             html.Br(),
#             html.Br(),
#             html.Div(msg[0], className='user-message'),
#             html.Br(),
#             html.Br(),
#             html.Div(msg[1], className='assistant-message'),
#             html.Br(),
#             html.Br()
#         ]) for msg in response]
        
#         # return the message components
#         return message_components
#     else:
#         return []
    
    
if __name__ == '__main__':  
    app.run_server()

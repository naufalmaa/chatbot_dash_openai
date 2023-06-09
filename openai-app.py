import openai
import dash
from dash import Dash
from dash import html
from dash import Input, Output, State, ctx
import dash_mantine_components as dmc
import time
from dash_iconify import DashIconify

# Set up OpenAI API credentials
openai.api_key = "###"

# create dash app
app = Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

# define the app layout in the section below
app.layout = html.Section([
    html.Div(id='input-container',
             children=[ # create text input
                        dmc.Textarea(
                            label='Say "Hi" first to our assistant!',
                            id='input-box',
                            className='input-text',
                            placeholder='Type your message here...',
                            autosize=True,
                            minRows=3,
                            maxRows=4
                        ),
                        # dmc.Loader(color="blue", size="md", id='loader', variant="dots"),
                        dmc.Button('Send', leftIcon = DashIconify(icon="ri:send-plane-fill", width=20), variant="filled", id='submit-button', className ='icon-button-1', color='indigo', n_clicks=0),
                        dmc.Button('Reset', leftIcon = DashIconify(icon="codicon:debug-restart", width=20), variant="filled", id='reset-button', className ='icon-button-2', color='red', n_clicks=0),
                        ]
            ),
    html.Div(className='output-text',
             children=[
                        dmc.LoadingOverlay(
                            html.Div(id="output-container")
                        )
                    ]
             )
])

# set history of messages
message_history = []

# define chatgptbot for generating messages
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

# define clear message history
def clear_history():
    
    global message_history
    
    message_history = []
    return message_history


# create callbacks
@app.callback(
    Output('output-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('input-box', 'value'),
)

#set update output
def update_output(b1,b2, value):
    
    # create attribute for button clicked
    button_click = ctx.triggered_id
    
    # input the messages using submit button
    if button_click == 'submit-button':
        # insert loading indicator
        time.sleep(2)
        
        # call the chatbot function to get the response
        response = chatbot(value)
        
        # create a list of message components for each response tuple
        message_components = [html.Div([
            html.Br(),
            html.Br(), 
            html.Div("You:", style={"color": "#112D4E", "font-weight": "bold"}),
            html.Div(msg[0], className='user-message'),
            html.Br(),
            html.Br(),
            html.Div("Assistant:", style={"color": "#112D4E","font-weight": "bold",  "display":"flex", "justify-content":"right", "align-items": "right"}),
            html.Div(msg[1], className='assistant-message', style={"display":"flex", "justify-content":"right", "align-items": "right"}),
            html.Br(),
            html.Br()
        ]) for msg in response]
        
        # return the message components
        return message_components
    
    # reset the history messages using reset button
    elif button_click == 'reset-button':
        # insert loading indicator
        time.sleep(2)
        
        clear_history()
        
        clear_components = [html.Div([
            html.Br(),
            html.P("Message cleared!"),
            html.Br()
        ])]
        
        return clear_components
    
    else:
        return []

if __name__ == '__main__':  
    app.run_server()

import openai
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Set up OpenAI API credentials
openai.api_key = "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"

# create dash app
app = dash.Dash(__name__)

# define the app layout in the section below
app.layout = html.Div([
    html.Div(id='message-container'),
    dcc.Input(
        id='user-input',
        type='text',
        placeholder='Type your message here...',
        autoComplete='off',
    ),
    html.Button('Send', id='submit-button', n_clicks=0),
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

# define the app callback
@app.callback(
    Output('message-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('user-input', 'value')],
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        # call the chatbot function to get the response
        response = chatbot(value)
        
        # create a list of message components for each response tuple
        message_components = [html.Div([
            html.Div(msg[0], className='user-message'), html.Br(),
            html.Div(msg[1], className='assistant-message')
        ]) for msg in response]
        
        # return the message components
        return message_components
    else:
        return []
    
if __name__ == '__main__':  
    app.run_server()
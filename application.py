import json
import requests
from creatomate import Animation, Image, Element, Composition, Source, Video, Audio

first_question = { 
    "question": "¿Cómo se dice \"música\" en inglés?",
    "options": ["Milk", "Music", "Mountain"],
    "correct": 1
}
second_question = { 
    "question": "¿Cómo se dice \"casa\" en inglés?",
    "options": ["House", "Hard", "Height"],
    "correct": 0
}

questions = [first_question, second_question]
background_images = [
    "https://creatomate.com/files/assets/4a6f6b28-bb42-4987-8eca-7ee36b347ee7",
    "https://images.unsplash.com/photo-1486010586814-abd061e90cf9?q=80&w=1374&auto=format&fit=crop"
]

text_start_anim = Animation(
    time="0 s",
    duration="1.5 s",
    easing="quadratic-out",
    type="text-slide",
    scope="split-clip",
    split="line",
    distance="100%",
    direction="up",
)

text_end_anim = Animation(
    time="end",
    duration="1 s",
    easing="quadratic-out",
    type="text-slide",
    direction="left",
    split="line",
    scope="element",
    distance="200%",
    reversed=True
)

comp_start_anim = Animation(
    time="start",
    duration="1 s",
    transition=True,
    type="wipe",
    fade=False,
    x_anchor="0%",
    end_angle="270°",
    start_angle="270°"
)

stroke_color = [{ "time": "0 s", "value": "#000000" }, { "time": "5.2 s", "value": "#000000" }, { "time": "5.5 s", "value": "#00ff00" }]

source = Source('mp4', 1080, 1920, "20 s")
background_music = Audio("Music", 18, "0 s", None, True, "b5dc815e-dcc9-4c62-9405-f94913936bf5", "51%", "2 s")
source.elements.append(background_music)
video = Video(source)

for index, question in enumerate(questions):
    composition = Composition("Question" + str(index), 1, "8 s")

    question_text = Element("text", track=2, text=question["question"], y="21.80%", fill_color="#000000", background_color="#ffffff")
    question_text.animations.append(text_start_anim)
    question_text.animations.append(text_end_anim)
    composition.elements.append(question_text)

    animation = Animation(easing='linear', type='scale', scope='element', start_scale='120%', fade=False)
    image = Image(background_images[index], 1, 10, True, [])
    image.animations.append(animation)
    composition.elements.append(image)

    counter = Image("06311a89-c770-48e1-8a33-b5c1c417c787", 9, 5, True, [], y="81.96%", width="26.062%", height="15.1904%")
    composition.elements.append(counter)

    countdown = Audio("countdown", 10, "0 s", "4.8 s", True, "3b591fe7-e995-4e18-9353-f38c122cc3fb", "100%", "0 s")
    composition.elements.append(countdown)
    correct = Audio("correct", 10, "4.90 s", "1.85 s", True, "530d3905-bd5b-4534-9532-f6657ed03296", "100%", "0 s")
    composition.elements.append(countdown)
    composition.elements.append(correct)

    if index > 0:
        composition.animations.append(comp_start_anim)

    for index, option in enumerate(question["options"]):
        position_y = 52 + (10 * index)
        option_text = Element("text", track=index + 3, text=option, y=str(position_y) + "%", fill_color="#ffffff")

        if index == question["correct"]:
            option_text.stroke_color = stroke_color
        else:
            option_text.stroke_color = "#000000"
        
        composition.elements.append(option_text)

    for i in range(5):
        countdown_text_number = Element("text", track=12, text=str(5 - i), x="54.90%", y="84.96%", z_index=1, time=i, duration="1 s", fill_color="#111111", font_size="15 vmin")
        composition.elements.append(countdown_text_number)

    source.elements.append(composition)

output = json.loads(video.toJSON())

response = requests.post(
 'https://api.creatomate.com/v1/renders',
 headers={
  'Authorization': 'Bearer 26b9c2989bee4a42a642450e143ed34e9ec39d1bebf5785e6cc82446ba2a69c4c3910b9be962f3e7cf7880c2d9eb550b',
  'Content-Type': 'application/json',
 },
 json=output
)
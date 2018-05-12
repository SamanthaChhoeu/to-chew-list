/*
 * Starter Project for Messenger Platform Quick Start Tutorial
 *
 * Remix this as the starting point for following the Messenger Platform
 * quick start tutorial.
 *
 * https://developers.facebook.com/docs/messenger-platform/getting-started/quick-start/
 *
 */

'use strict';

const ACCESS_PROD_KEY = process.env.PAGE_ACCESS_TOKEN;

// Imports dependencies and set up http server
const 
  request = require('request'),
  express = require('express'),
  body_parser = require('body-parser'),
  axios = require('axios'),
  app = express().use(body_parser.json()); // creates express http server

//subs list
let subs = [];

// Sets server port and logs message on success
app.listen(process.env.PORT || 1337, () => console.log('webhook is listening'));

// Accepts POST requests at /webhook endpoint
app.post('/webhook', (req, res) => {  
  // Parse the request body from the POST
  let body = req.body;
  // Check the webhook event is from a Page subscription
  if (body.object === 'page') {
    // Iterate over each entry - there may be multiple if batched
    body.entry.forEach(function(entry) {
      if (entry.messaging){
        // Get the webhook event. entry.messaging is an array, but 
        // will only ever contain one event, so we get index 0
        let webhook_event = entry.messaging[0];
        // Get the sender PSID
        let sender_psid = webhook_event.sender.id;

        // Check if the event is a message or postback and
        // pass the event to the appropriate handler function
        if (webhook_event.message) {
          handleEvent(sender_psid, webhook_event.message);
        } else if (webhook_event.postback) {
          handlePostback(sender_psid, webhook_event.postback);
        }
      }
    });
    // Return a '200 OK' response to all events
    res.status(200).send('EVENT_RECEIVED');
  } else {
    // Return a '404 Not Found' if event is not from a page subscription
    console.log("NOT FOUND")
    res.sendStatus(404);
  }
});

// Accepts GET requests at the /webhook endpoint
// app.get('/webhook', (req, res) => {
//   console.log("WEBHOOK GET");
//   const VERIFY_TOKEN = ACCESS_PROD_KEY;
  
//   // Parse params from the webhook verification request
//   let mode = req.query['hub.mode'];
//   let token = req.query['hub.verify_token'];
//   let challenge = req.query['hub.challenge'];
    
//   // Check if a token and mode were sent
//   if (mode && token) {
//     // Check the mode and token sent are correct
//     if (mode === 'subscribe' && token === VERIFY_TOKEN) {
//       // Respond with 200 OK and challenge token from the request
//       console.log('WEBHOOK_VERIFIED');
//       res.status(200).send(challenge);
//     } else {
//       // Responds with '403 Forbidden' if verify tokens do not match
//       console.log('FORBIDDEN');
//       res.sendStatus(403);  
//     }
//   // Else return 404
//   } else {
//     res.sendStatus(404).send("NOT FOUND");
//   }
// });

function subbed(sender_psid){
  for(let i = 0; i < subs.length; i++){
    if (subs[i] === sender_psid){
      return true;
    }
  }
  return false;
}

//handles all the events
function handleEvent(sender_psid, received_message){
  if(received_message.text == "!help") {
    handleHelp(sender_psid);
  } else if (!subbed(sender_psid)){
    ask_sub(sender_psid);
  } else if (received_message.text == "!unsubscribe") {
    let index = subs.indexOf(sender_psid);
    if (index > -1) {
      subs.splice(index, 1);
      let response = {"text":"You have unsubscribed"};
      callSendAPI(sender_psid, response);
    }
  }else {
    topicQuery(sender_psid, received_message.text);
  }
}

//This function will print helpful commands
function handleHelp(sender_psid) {
  let response = {"text":"!help - prints out useful commands\n"
                  + "!unsubscribe - unsubscribe from PaperBoy\n\n"
                  + "Type any of the following categories to get the top 3 related stories:\n"
                  + "📰 Top Headlines \n"
                  + "🌏 World \n"
                  + "📈 Business \n"
                  + "📍 Nation \n"
                  + "🔬 Science\n"
                  + "💻 Tech \n"
                  + "💼 Politics\n"
                  + "🎫 Entertainment \n"
                  + "🏀 Sport \n"
                  + "🚑 Health \n"
                  + "\nOtherwise feel free to ask for news on any other topic!\n"
                 };


  callSendAPI(sender_psid, response);
}



function topicQuery(sender_psid, query){
  let response = {"text":"Here are your results for: "+query};
  callSendAPI(sender_psid, response);
  let conf = { headers: {"x-api-key": "9KwLp0ApWBaxOGwfqH9Pg5gw0DNZ7ze36q0N8hAF", "Content-Type": "application/json"} }
  axios.post("https://j0l0kn7khi.execute-api.us-east-1.amazonaws.com/prod/query", { "query": query }, conf)
  .then(function (responses) {
    responses = JSON.parse(responses.data.articles);
    callSendAPI(sender_psid, list_maker(responses));
  }).catch(function (error) {
    // console.error(error.response.status);
  });
}


// Handles messaging_postbacks events
function handlePostback(sender_psid, received_postback) {
  let response;
  // Get the payload for the postback
  let payload = received_postback.payload;

  // Set the response based on the postback payload
  if (payload === 'yes') {
    subs.push(sender_psid);
    // console.log(subs);
    headline_response(sender_psid);
  } else if (payload === 'no') {
    response = { "text": "Sorry to disturb you! :'(" }
    callSendAPI(sender_psid, response);
  } else {
    topicQuery(sender_psid, payload);
  }
}

// Sends response messages via the Send API
function callSendAPI(sender_psid, response) { 
  axios.post("https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_PROD_KEY, 
    {
      "recipient": { "id": sender_psid },
      "message": response
    }
  ).then(function (response) {
    // console.log("sent");
  }).catch(function (error) {
    // console.log(error.response.status);
  });
}

// A starter sub box
function ask_sub(sender_psid){
  let question = {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
        "elements": [{
          "title": "Welcome to Paper Boy!",
          "subtitle": "Would you like to subscribe to daily news?\n For help type !help",
          "image_url": "https://cdn.glitch.com/7b88e027-f126-4d88-8c93-870e7842d10a%2FYes_No.png?1526080992938",
          "buttons": [
            {
              "type": "postback",
              "title": "Yes!",
              "payload": "yes",
            },
            {
              "type": "postback",
              "title": "No!",
              "payload": "no",
            }
          ],
        }]
      }
    }
  }
  callSendAPI(sender_psid, question);
}

// Handles headline message creation
function headline_response(sender_psid) {
  let response = {"text":"🌞 GOOD MORNING, here's what's trending today! 🙏☀️"}
  callSendAPI(sender_psid,response);
  axios.get("https://j0l0kn7khi.execute-api.us-east-1.amazonaws.com/prod/headlines")
    .then(function (ret) {
      ret = JSON.parse(ret.data.articles);
      callSendAPI(sender_psid, list_maker(ret));
    })
    .catch(function (error) {
      // console.log(error);
    }); 
  let help = {"text":"Use !help for more commands"}
  callSendAPI(sender_psid,help);
}

//pushes generic card into a list template
function list_maker(newsList){
  let cards = [];
  newsList.forEach(function (ret) {cards.push(card_maker(ret))});
  return ({
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"list",
        "top_element_style": "large",
        "elements": cards
      }
    }
  });
}

//Makes generic card
function card_maker(news){
  return ({
    "title":news.title,
    "image_url": (news.image !== null) ? news.image : "https://i.imgur.com/LEYU3bs.png",
    "subtitle": news.source,
    "default_action": {
      "type": "web_url",
      "url": news.link,
      "messenger_extensions": false,
      "webview_height_ratio": "FULL"
    },
  });
}
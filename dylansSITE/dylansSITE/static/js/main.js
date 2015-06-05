var recognizer;
var recorder;
var callbackManager;
var audioContext;

// Only when both recorder and recognizer are ready do we have a ready application
// I'm keeping these so I can use them with other applications
var recorderReady = false;
var recognizerReady = false;

var keywordIndicator = document.getElementById('recording_indicator');

// TEMP
var outputContainer;

// the phones we want to detect
var wordList = [
    ["ONE", "W AH N"],
    ["CHEESE", "CH IY Z"],
    ["TWO", "T UW"],
    ["THREE", "TH R IY"],
    ["FOUR", "F AO R"],
    ["FIVE", "F AY V"],
    ["SIX", "S IH K S"],
    ["SEVEN", "S EH V AH N"],
    ["EIGHT", "EY T"],
    ["NINE", "N AY N"],
    ["ZERO", "Z IH R OW"],
    ["NEW-YORK", "N UW Y AO R K"],
    ["NEW-YORK-CITY", "N UW Y AO R K S IH T IY"],
    ["PARIS", "P AE R IH S"],
    ["PARIS(2)", "P EH R IH S"],
    ["SHANGHAI", "SH AE NG HH AY"],
    ["SAN-FRANCISCO", "S AE N F R AE N S IH S K OW"],
    ["LONDON", "L AH N D AH N"],
    ["BERLIN", "B ER L IH N"],
    ["SUCKS", "S AH K S"],
    ["ROCKS", "R AA K S"],
    ["IS", "IH Z"],
    ["NOT", "N AA T"],
    ["GOOD", "G IH D"],
    ["GOOD(2)", "G UH D"],
    ["GREAT", "G R EY T"],
    ["WINDOWS", "W IH N D OW Z"],
    ["LINUX", "L IH N AH K S"],
    ["UNIX", "Y UW N IH K S"],
    ["MAC", "M AE K"],
    ["AND", "AE N D"],
    ["AND(2)", "AH N D"],
    ["O", "OW"],
    ["S", "EH S"],
    ["X", "EH K S"]
];

var grammars = [{
    g: {
        numStates: 1,
        start: 0,
        end: 0,
        transitions: [
        {
            from: 0,
            to: 0,
            word: "ONE"
        }, 
        {
            from: 0,
            to: 0,
            word: "CHEESE"
        }, {
            from: 0,
            to: 0,
            word: "TWO"
        }, {
            from: 0,
            to: 0,
            word: "THREE"
        }, {
            from: 0,
            to: 0,
            word: "FOUR"
        }, {
            from: 0,
            to: 0,
            word: "FIVE"
        }, {
            from: 0,
            to: 0,
            word: "SIX"
        }, {
            from: 0,
            to: 0,
            word: "SEVEN"
        }, {
            from: 0,
            to: 0,
            word: "EIGHT"
        }, {
            from: 0,
            to: 0,
            word: "NINE"
        }, {
            from: 0,
            to: 0,
            word: "ZERO"
        }
        ]
    }
}];

// When the page is loaded we spawn a new recognizer worker and call getUserMedia to request access to the microphone
window.onload = function() {

    recognizer = new Worker('/static/js/recognizer.js');

    callbackManager = new CallbackManager();

    // TEMP
    outputContainer = document.getElementById("output");
    // document.getElementById('start_button').onclick = startRecording;

    // initialize Web Audio variables
    try {

    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    window.URL = window.URL || window.webkitURL;

    audioContext = new AudioContext();

    } catch (e) {
        // report incompatible browser
    }

    if (navigator.getUserMedia) {

    navigator.getUserMedia({
        audio: true
    }, function(stream) {

    var input = audioContext.createMediaStreamSource(stream);

    var audioRecorderConfig = {
        errorCallback: function(x) {}
    };

    recorder = new AudioRecorder(input, audioRecorderConfig);

    // If a recognizer is ready we pass it to the recorder
    if (recognizer) {
        recorder.consumers = [recognizer];
    }

    recorderReady = true;

    }, function(e) {

    });

    }

    recognizer.onmessage = function() {

    // I need this nested event listener because the first time a message is triggered we need to trigger other things that we never need to trigger again
    recognizer.onmessage = function(e) {

    // if an id to be used with the callback manager
    // this is needed to start the listening
    if (e.data.hasOwnProperty('id')) {

        var data = {};
    
        if (e.data.hasOwnProperty('data')) {
            data = e.data.data;
        }
    
        var callback = callbackManager.get(e.data['id']);
    
        if (callback) {
            callback(data);
        }

    }

    // if a new hypothesis has been created
    if (e.data.hasOwnProperty('hyp')) {

        var hypothesis = e.data.hyp;
    
        if (outputContainer) {
            //window.alert(hypothesis)
            outputContainer.innerHTML = hypothesis;            
            
        }
        
        

    }

    // if an error occured
    if (e.data.hasOwnProperty('status') && (e.data.status == "error")) {

    }

    };

    // Once the worker is fully loaded, we can call the initialize function
    // You can pass parameters to the recognizer, such as : {command: 'initialize', data: [["-hmm", "my_model"], ["-fwdflat", "no"]]}
    postRecognizerJob({
        command: 'initialize'
    }, function() {

        if (recorder) {
            recorder.consumers = [recognizer];
        }
    
        postRecognizerJob({
            command: 'addWords',
            data: wordList
        }, function() {
            feedGrammar(grammars, 0);
    
        startRecording();
    
        });

    });

    };

    recognizer.postMessage('');

};

function postRecognizerJob(message, callback) {

    var msg = message || {};

    if (callbackManager) {
        msg.callbackId = callbackManager.add(callback);
    }

    if (recognizer) {
        recognizer.postMessage(msg);
    }

}

function feedGrammar(g, index, id) {

    if (index < g.length) {

    postRecognizerJob({
        command: 'addGrammar',
        data: g[index].g
    }, function(id) {
        feedGrammar(grammars, index + 1, {
            id: id
        });
    });

    } else {
        recognizerReady = true;
    }

}

// This starts recording. We first need to get the id of the grammar to use
function startRecording() {
    if (recorder && recorder.start(0)) {
        keywordIndicator.style.display = 'block';
    }
}
console.log('Page Loading...');
// variable declarations.
let user = null;
let currentRoom = null;

//  brings in the socket from the cdn link.
const socket = io();

// targeted DOM elements.
const currentChat = document.getElementById('current_chat');
const roomDisplay = document.getElementById('current_room');
const joinedRoomList = document.getElementById('rooms_joined');


// function declarations
function jsonFetch(request, callback, where=null) {
    fetch(request)
        .then(response=> {
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                callback(null, new TypeError(`Content-Type is non-json: ${contentType}`));
            } else
                return response.json();
        })
        .then(data => callback(data, null))
        .catch(err => console.error(`jsonFetch Error: ${where === null ? '' : where}`, err));
}


//async function to retrieve the logged in user's info and join them to their list of joined rooms
//we call this function on connect
async function getUser() {
        let response = await fetch('/api/users/get_logged_user')
        console.log(response);
        let user_data = await response.json()
        user = user_data
        console.log(user)
        for (let room_id of user.joined_room_ids) {
            console.log('joining ', room_id)
            joinRoom(room_id)
        }
}



//function for joining a previously joined room (room in our room list)
function joinRoom(room_id) {
    socket.emit('join', {
        username: user.username,
        room: "" + room_id
    })
}

// function for joining a new room (adds it to our room list)
function joinNewRoom(room_id) {
    if (user.joined_room_ids.includes(room_id)){
        alert('Already joined')
        return
    }
    user.joined_room_ids.push(room_id)
    joinRoom(room_id)
    jsonFetch('/api/rooms/' + room_id + '/join' ,  err => {
        if (err !== null){
            console.log('Join History', err);
            return
        }
        joinedRoomList.innerHTML += `
        <div class="flex flex-row justify-center gap-4 cursor-pointer" id="joined${room_id}" >
            <p class="text-blue-900 underline underline-offset-1" onclick="getHistory(${room_id})" ><span id="newFor${room_id}" class="text-red-600"></span> ${data.roomname} </p>
            <button type="submit" onclick="leaveRoom(${room_id})" class="bg-red-600 hover:bg-red-300 text-white p-2 rounded-lg" >Leave</button>
        </div>
        `
    }, 'Get Join History');
}

// function for leaving a room
function leaveRoom(room_id) {
    socket.emit('leave', {
        username: user.username,
        room: "" + room_id
    })
    user.joined_room_ids = user.joined_room_ids.filter(e => e != room_id)
    fetch('/api/rooms/' + room_id + '/leave')
        .then(res => res.json())
        .then(data => {
            console.log(data)
            document.getElementById("joined" + room_id).remove()

        })
        .catch(err => console.log(err))
}

function send(event){
    event.preventDefault();
    if(currentRoom === null){
        alert('Select a room to continue.');
    }
    let message_content = event.target.message.value;
    let message = {'username': user.username, 'content': message_content, 'created_at': new Date().toLocaleString('en-US')};
    socket.emit('new_message', message, currentRoom);
    event.target.message.value = '';
    console.log(message_content);
    console.log(message);
    console.log(socket.emit('new_message', message, currentRoom));
}

//function for retrieving a room's history from the db and displaying it to page
function getHistory(room_id) {
    currentRoom = room_id;
    newSpan = document.getElementById("newFor" + room_id);
    newSpan.innerText = "";
    jsonFetch(`/api/rooms/${room_id}/history`, (data, err) => {
        if (err !== null) {
            console.log('History Error:', err);
            return
        }
        console.log('history', data);
        roomDisplay.innerHTML = data.history[0].name //todo: pass roomname from py in response.
        renderChat(data.history);
    }, 'get history error');
}

//helper function to render chat history, gets called in getHistory
function renderChat(chat_log) {
    currentChat.innerHTML = "<p>Loading...</p>"
    //updating the DOM is expensive, so it's better to generate all the HTML and then set it only once
    let chatHTML = ""
    for (let message of chat_log) {
        chatHTML += `
        <p>${message.username} at ${message.created_at}: ${message.content}</p>
        `
    }
    currentChat.innerHTML = chatHTML
    currentChat.lastElementChild.scrollIntoView(); //this line scrolls our chat to the bottom
}

// socket event. connectoin happens when client  connect to server. we collect user data at this time.
socket.on('connect', () => {
    console.log(socket.id);
    getUser();
})

socket.on('message_added', (message, roomFor) => {
    console.log('received message from server for room ' + roomFor)
    if (roomFor == currentRoom) { //if we got a message for the room we're currently viewing
        //we add it to the current chat view, and scroll to the bottom
        currentChat.innerHTML +=
        `
        <p>${message.username} at ${message.created_at}: ${message.content}</p>
        `
        console.log(currentChat.lastElementChild);
        currentChat.lastElementChild.scrollIntoView();
    } else {
        // if it's for a room we've joined but aren't viewing, we add or increment the badge next to the room
        newSpan = document.getElementById("newFor" + roomFor)
        console.log(newSpan)
        if (newSpan.innerText == "") {
            newSpan.innerText = '1';
        } else {
            newSpan.innerText++;
        }
    }
})

//if a user joins the room we're viewing, this displays that in the chat
socket.on('user_join', (username, room) => {
    console.log(username + " joined " + room)
    if (room == currentRoom) {
        currentChat.innerHTML += `<p>${username} has joined us live</p>`
        currentChat.lastElementChild.scrollIntoView();
    }
})

//if a user leaves the room we're viewing, this displays that in the chat
socket.on('user_leave', (username, room) => {
    console.log(username + " left " + room)
    if (room == currentRoom) {
        currentChat.innerHTML += `<p>${username} has disconnected</p>`
        currentChat.lastElementChild.scrollIntoView();
    }
})

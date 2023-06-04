console.log('Page Loading...');
// these variables will keep track of our user data and the current room we're watching
let user = null;
let currentTeam = null;
// these variables will listen for form submission and each user
let reg_btn = document.getElementById('reg_btn');
let log_btn = document.getElementById('log_btn');


// targeted variables
const currentChat = document.querySelector('.current_chat');
console.log('Testing display of current chat area:', currentChat)

var socket = io({autoConnect: False});
// eventlisteners for the reg and log form.
reg_btn.addEventListener('click', (e) => {
    e.preventDefault();
    let username = document.getElementById('username').vaule;
});
log_btn.addEventListener('click', (e) => {
    e.preventDefault();
    let username_log = document.getElementById('username_log').value;
});
// async function ot tetrieve the logged in user's info and join to their list of joined rooms
// we call this function on connect
async function getUser(){
    let res = await fetch('api/user/get_logged_user')
    let user_data = await res.json();
    user = user_data;
    console.log(user);
    for (let team_id of user.team_joined_ids){
        console.log('joining', team_id)
        joinTeam(team_id)
    }
}
// function for joining a team
function joinTeam(team_id){
    socket.emit('join', {
        username: user.username,
        team: "" + team_id
    })
}

socket.connect();

socket.on('connect', () => {
    socket.emit('user_reg', username);
});


// eventlisteners for the messages/chats.
socket.on('message', (message) => {
    var container = document.getElementById('message-container');
    var messageElement = document.createElement('p');
    messageElement.innerText = message;
    container.appendChild(messageElement);
});

var form = document.getElementById('message-form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    var input = document.getElementById('message-input');
    var message = input.value;
    socket.emit('message', message);
    input.value = '';
});
window.addEventListener('DOMContentLoaded', () => {
    let data = [];
    let socket = io();
    socket.on('response', (msg) => {
        data.length = 0
        data.push(...msg)
    })
    Vue.use(VueTables.ClientTable);
    new Vue({
    el: "#app",
    data: {
        columns: ['email', 'diamond', 'status'],
        data: data,
        options: {
        editableColumns:['email', 'diamond', 'status'],
        sortable: ['email', 'diamond', 'status'],
        filterable: ['email', 'diamond', 'status'],
        }
    }
    });


})
$("#submit").on("click", (e)=>{
    let action = $("#submit").data('action') // Extract info from data-* attributes648
    data = $("#form").serializeArray()
    res = {areas:[]}
    data.forEach(e=>{
        if(e.value!="on")res[e.name] = e.value
        else res.areas.push(e.name)
    })
    if(action == "addUser" && (res.name == "" || res.pseudo == "")){
        $("#errorMissingName").collapse("show")
        return
    }else if(action == "editUser"){
        res.oldPseudo = $("#submit").data('pseudo')
    }
    fetch(action == "addUser"?"http://127.0.0.1:8080/newMemb":"http://127.0.0.1:8080/editUser", {
        mode:"cors",
        method:"POST",
        body:JSON.stringify(res)
    }).then(e=>e.json()).then(e=>{
        if(e.response == "alreadyTaken")$("#errorUserTaken").collapse("show")
        else if(e.response == "ok")$(action == "addUser"?"#userCreated":"#userUpdated").collapse("show")
        if(e.code == 0){
            refresh()
            setTimeout(()=>{$("#addUserModal").modal('hide')}, 400)
        }
    })
})

$('form input').keydown(function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        refresh()
        return false;
    }
});

function refresh(){
    $("#tbody").empty()
    fetch("http://127.0.0.1:8080/getUsers",{
        mode:"cors", 
        method: 'POST',
        body:$("#searchBox").val()
    }).then(e=>e.json()).then(e=>{
        console.log(e)
        addUsers(e)
    })
    return false
}
refresh()

$(".refresh").on('click', ()=>{
    console.log("re")
    refresh()
})
function addUsers(users){
    let c = false
    users.forEach(user=>{
        c = !c
        var area = ""
        console.log(user.Areaofinterests)
        user.Areaofinterests.forEach(e=>area = area + e + ", ")
        area = area.slice(0, -2)
        $("#tbody").append(`
        <tr ${c?'class="table-secondary"':""} id=${user.Username}>
            <th scope="row">${user.Name}</th>
            <td>${user.Username}</td>
            <td>${user.Age}</td>
            <td>${user.YearofStudy}</td>
            <td>${user.FieldofStudy}</td>
            <td>${user.City}</td>
            <td>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#listOfUserModal" data-type="followers" data-user="${user.Name}" data-list='${JSON.stringify(user.followers)}'>Followed By</button>
                <div class="btn-group">
                    <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#listOfUserModal" data-type="iFollow" data-user="${user.Name}" data-list='${JSON.stringify(user.iFollow)}'>Follows</button>
                    <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#listOfUserModal" data-type="editFollows" data-user="${user.Name}" data-list='${JSON.stringify(user.iFollow)}' data-username="${user.Username}">Edit</button>
                </div>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-toggle="modal" data-target="#listOfUserModal" data-type="suggestion" data-user="${user.Name}" data-list='${JSON.stringify(user.suggestions)}')">Suggestions</button>
            
            </td>
            <td>
                <button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="${area}">
                    Hover to display
                </button>
            </td>
            <td>
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#addUserModal" data-action="editUser" data-pseudo=${user.Username} data-user='${JSON.stringify(user)}'>Edit</button>
                <button type="button" class="btn btn-primary" onclick="del('${user.Username}')">Delete</button>
            </td>
        </tr>`)
        $(function () {
            $('[data-toggle="tooltip"]').tooltip()
        })
    })
}

function del(user){
    if(!confirm("/!\\ are you sure to delete " + user + " ?")) return
    console.log(user)
    fetch("http://127.0.0.1:8080/delUser", {
        mode:"cors",
        method:"POST",
        body:JSON.stringify({username:user})
    }).then(()=>refresh())
}


$('#listOfUserModal').on('show.bs.modal', (event)=>{
    var button = $(event.relatedTarget) // Button that triggered the modal
    var list = button.data('list') // Extract info from data-* attributes648
    var type = button.data("type")
    function redraw(type, list){
        $("#listOfUserModal .modal-body").empty()
        if(type=="followers"){
            $("#listOfUserModal .modal-header").text(`followers of ${button.data("user")}`)
            if(list.length == 0){
                $('#listOfUserModal .modal-body').append("<p><i>This user doesn't have any followers</i></p>")
            }
        }else if(type=="iFollow" || type=="editFollows"){
            $("#listOfUserModal .modal-header").text(`Users followed by ${button.data("user")}`)
            if(list.length == 0){
                $('#listOfUserModal .modal-body').append("<p><i>This user doesn't follow anyone</i></p>")
            }
        }else if(type=="suggestion"){
            $("#listOfUserModal .modal-header").text(`suggestion for ${button.data("user")}`)
            if(list.length == 0){
                $('#listOfUserModal .modal-body').append("<p><i>We could not found any suggestion for this user</i></p>")
            }
        }
        $('#listOfUserModal .modal-body').append('<div class="list-group">')
        list.forEach(user=>{
            $('#listOfUserModal .modal-body').append(`
            <div class="list-group-item clearfix">
            <a href="" class="stretched-link" onclick="highlight('${user}');">${user}</a>
            ${type=="editFollows"?`<span class="float-right">
            <button class="btn removeUser" data-toremove=${user} >remove</button>
            </span>`:``}
            </div>
            `)
        })
        $('#listOfUserModal .modal-body').append("</div>")
        $(".removeUser").on("click", (e)=>{
            fetch("http://127.0.0.1:8080/follow", {
                mode:"cors",
                method:"POST",
                body:JSON.stringify({user:button.data("username"), userToFollow:$(e.target).data("toremove"), follow:false})
            }).then(r=>r.json()).then(r=>{
                if(r.response == "notFound"){
                    $("#errorUserNotFound").collapse("show")
                }
                if(r.code==0){
                    redraw(type, r.newList)
                }
            })
        })
        
        $("#submitFollows, #submitFollowsBox").remove()
        if(type=="editFollows"){
            $('#listOfUserModal .modal-footer').prepend(`<button type="button" class="btn btn-primary mr-auto" id="submitFollows">Add User</button>`)
            $('#listOfUserModal .modal-footer').prepend(`<input class="form-control mr-sm-2" type="search" placeholder="Follow a new user" aria-label="Follow a new user" id="submitFollowsBox">`)
            $("#submitFollows").on("click", ()=>{
                fetch("http://127.0.0.1:8080/follow", {
                    mode:"cors",
                    method:"POST",
                    body:JSON.stringify({user:button.data("username"), userToFollow:$("#submitFollowsBox").val(), follow:true})
                }).then(r=>r.json()).then(r=>{
                    if(r.response == "notFound"){
                        $("#errorUserNotFound").collapse("show")
                    }
                    if(r.code==0){
                        redraw(type, r.newList)
                    }
                })
            })
        }
    }
    redraw(type, list)
})


$('#addUserModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var action = button.data('action')
    var modal = $(this)
    if(action == "addUser"){
        modal.find(".modal-header").text("Add User Form")
        $("#form input[name=pseudo]").attr("disabled", false)
        $("#submit").data("action", "addUser")
    }else if(action == "editUser"){
        var user = button.data("user")
        $("#submit").data('pseudo', user.Username)
        modal.find(".modal-header").text(`Editing ${user.Name}`)
        $("#form input[name=name]").val(user.Name)
        $("#form input[name=age]").val(user.Age)
        $("#form input[name=year]").val(user.YearofStudy)
        $("#form input[name=field]").val(user.FieldofStudy)
        $("#form input[name=pseudo]").val(user.Username)
        $("#form input[name=pseudo]").attr("disabled", true)
        $("#form input[name=city]").val(user.City)
        $(`#form input[type=checkbox]`).prop( "checked",false );
        user.Areaofinterests.forEach(area=>{
            $(`#form input[name=${area}]`).prop( "checked", true );
        })
        $("#submit").data("action", "editUser")
    }
})
function highlight(user){
    console.log(user)
    $('#listOfUserModal').modal("hide")
    let lastclass = $(`#${user}`)[0].className
    $(`#${user}`)[0].className = "table-success"
    setTimeout(()=>{$(`#${user}`)[0].className = lastclass}, 3000)
}
$('#listOfUserModal').on('hide.bs.modal', (event)=>{
    $("#listOfUserModal .modal-body").empty()
    refresh()
})
$("#addUser").on("click", ()=>{
    $("#form").trigger("reset")
})
$(".collapse").on("show.bs.collapse", (e)=>{
    $(`.collapse:not(#${e.target.id})`).collapse("hide")
    setTimeout(()=>{
        $(`#${e.target.id}`).collapse("hide")
    }, 2000) 
})

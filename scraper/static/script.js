$(document).foundation();
$(document).ready(function () {
    // $.ajax({
    //     type: 'POST',
    //     url: '/',
    //     success: function (response) {
    //         result.innerHTML = response.html
    //     }
    // })

    const searchbar = document.getElementById('search');
    const result = document.getElementById('result')
    searchbar.addEventListener('keyup', function(e) {
        query = e.target.value
        $.ajax({
            type: 'POST',
            url: '/live-search',
            data: JSON.stringify({'query': query}),
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                result.innerHTML = response.html
            }
        })
    })

    
    const categoryLinks = document.getElementsByClassName('category')
    const loadingGif = document.getElementById('loading')
    const alert = document.getElementById('alert')    

    for (var i = 0; i < categoryLinks.length; i++) {
        categoryLinks[i].addEventListener('click', function(e) {
            var category = this.innerHTML
            $.ajax({
                type: 'POST',
                url: '/load-category',
                data: JSON.stringify({'category': category}),
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    result.innerHTML = response.html
                    console.log(response)
                }
            })
            }
            
        )
     }
     const updateDatabase = document.getElementById('update-database')
     updateDatabase.addEventListener('click', function () {
        loadingGif.style.display = "block"
        $.ajax({
            type: 'POST',
            url: '/update-database',
            success: function(response) {
                loadingGif.style.display = 'none';
                alert.innerHTML = `<p>${response.alert}</p>`
                setTimeout(function() {
                    alert.innerHTML = ''
                }, 3000)
                result.innerHTML = response.html
            }
        })
     })

})

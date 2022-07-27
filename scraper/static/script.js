$(document).foundation();
$(document).ready(function () {
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
            loadingGif.style.display = "block"
            $.ajax({
                type: 'POST',
                url: '/load-category',
                data: JSON.stringify({'category': category}),
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    loadingGif.style.display = "none"
                    alert.innerHTML = `<p>${response.alert}</p>`
                    setTimeout(function() {
                        alert.innerHTML = ''
                    }, 3000)
                }
            })
            }
            
        )
     }

})

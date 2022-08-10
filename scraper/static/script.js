$(document).foundation();
$(document).ready(function () {
    // Get all categories available
    var CATEGORIES;
    $.ajax({
        type: 'POST',
        url: '/get-categories',
        success: function (response) {
            CATEGORIES = Object.keys(response)
        }
    })
    

    // Update html every time the text input changes
    const searchbar = document.getElementById('search');
    const result = document.getElementById('result')
    searchbar.addEventListener('keyup', function(e) {
        var query = e.target.value
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

    // Load category based on the <a>'s innerHTML
    const categoryLinks = document.getElementsByClassName('category')
    const loadingGif = document.getElementById('loading')  

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
     var updateDatabase = document.getElementById('update-database')
     updateDatabase.addEventListener('click', function () {
        loadingGif.style.display = "block"
        updateDatabase.setAttribute('disabled', 'disabled');

        $.ajax({
            type: 'POST',
            url: '/delete-database',
            success: function() {
                console.log('Succesfuly deleted all database.')
                
            }
        })

        function fetchLoop(i) {
            if (CATEGORIES.length == i) {
                console.log('Finished fetch loop with success.')
                loadingGif.style.display = "none"
                updateDatabase.removeAttribute('disabled')
                return;
            }
            $.ajax({
                type: 'POST',
                url: '/update-database',
                data: JSON.stringify({'category': CATEGORIES[i]}),
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                    
                },
                complete: function() {
                    i++
                    fetchLoop(i)
                    console.log(`Finished scraping category ${CATEGORIES[i]}`)
                }
            })
        }

        fetchLoop(0)
        
     })


})

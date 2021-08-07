const searchForm = document.querySelector('#searchForm')
const pageLinks = document.querySelectorAll('.page-link')
if (searchForm) {
    for (link of pageLinks) {
        link.addEventListener('click', function (event) {
            event.preventDefault()
            const page = this.dataset.page
            searchForm.innerHTML += `<input value=${page} name="page" hidden />`
            searchForm.submit()
        })
    }
}
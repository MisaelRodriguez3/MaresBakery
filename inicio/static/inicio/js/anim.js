const sr = ScrollReveal({
    distance: '60px',
    duration: 3000,
    // reset: true,
})


sr.reveal(`.about__data`,{
    origin: 'left',
})

sr.reveal(`.about__img-overlay`,{
    origin: 'right',
    interval: 100,
})

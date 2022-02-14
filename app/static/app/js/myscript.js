$('#slider1, #slider2, #slider3,#slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-quantity').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    var ch=this.parentNode.parentNode.children[3].children[1].children[0].children[0].children[0]

    $.ajax({
        type:"GET",
        url:'/increase_quantity',
        data:{
            pro_id : id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.totalPrice
            document.getElementById('totalAmount').innerText = data.totalAmount
            ch.innerText =data.priceForItem


        }
    })
})
$('.minus-quantity').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    var ch=this.parentNode.parentNode.children[3].children[1].children[0].children[0].children[0]
    $.ajax({
        type:"GET",
        url:'/reduce_quantity',
        data:{
            pro_id : id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.totalPrice
            document.getElementById('totalAmount').innerText = data.totalAmount
            ch.innerText =data.priceForItem
            console.log(data.priceForItem)
        }
    })
})


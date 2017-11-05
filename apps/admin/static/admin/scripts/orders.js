$(document).ready(function(){
    $('#customer').click(function(){
        $('#searchInput').html('<form action="orderSearch" method="post"><input type="hidden" name="search_type" value="customer"><input type="text" name="search"><input type="submit" value="Search by Customer Name"></form>')
    })
    $('#game').click(function(){
        $('#searchInput').html('<form action="orderSearch" method="post"><input type="hidden" name="search_type" value="game"><input type="text" name="search"><input type="submit" value="Search by Game"></form>');
    })
    $('#dateRange').click(function(){
        $('#searchInput').html('<form action="orderSearch" method="post"><input type="hidden" name="search_type" value="dateRange"><label for="start">From:</label><input type="date" name="start" id="start"><label for="end">To:</label><input type="date" name="end" id="end"><input type="submit" value="Search by date range"></form>');
    })
    $('#orderId').click(function(){
        $('#searchInput').html('<form action="orderSearch" method="post"><input type="hidden" name="search_type" value="orderId"><input type="text" name="search"><input type="submit" value="Search by Order Id"></form>')
    })
})
function WriteToEmail() {
    // get value of the banner selected by user
    var bvalue = $('#banner option:selected').val();
    // find alignment chosen by the user 
    var align = $('input[name="email-align"]:checked').val();
    var objO = new ActiveXObject('Outlook.Application');
    var objNS = objO.GetNameSpace('MAPI');
    var mItm = objO.CreateItem(0);
    mItm.Display();
    mItm.Subject = $('#title').val();
    mItm.GetInspector.WindowState = 2;
    mItm.HTMLBody = /* ************ HTML TOPPINGS ************ */
        "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'><html xmlns='http://www.w3.org/1999/xhtml'><body leftmargin='0' marginwidth='0' topmargin='0' marginheight='0' offset='0'><TABLE width='650' cellpadding='0' cellspacing='0' border='0' valign='top' align=" + align + "'>"
        /* ************ HEADER IMAGE ************ */
        + "<TR><TH align='center' ><img src='http://www.southerncompany.info/promos/email-generator-banners/" + bvalue + ".jpg' alt='My Banner' ></TH><TR>"
        /* ************ MAIN BODY ************ */
        + "<TR><TD style='padding: 20px 20px 10px 20px' valign='top' height='500'>" + CKEDITOR.instances.para_text.getData() + "</TD></TR></TABLE>";

}

//run when all the contents of the page have loaded
$(function() {
    //display banner image under the dropdown
    $('#banner').change(function() {
        $(".pop-img").remove();
        /*use this instead to be able to use your own images
        var banner = $('#banner option:selected').val();*/
      var banner = "650x153";
        if (banner != 'default') {
            $('#banner').after("<div class='pop-img'><img src='http://placehold.it/" + banner + ".jpg' alt='My Banner' ></div>");
        }
    });
});

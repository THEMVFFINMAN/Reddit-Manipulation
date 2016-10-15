time = 1000;
$(".option.active.remove.login-required").each(function() {
    time += 1000;
    window.setTimeout(function() {
        $($(".option.active.remove.login-required")[0]).click();
    }, time);
});

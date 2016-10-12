time = 1000
$(".option.active.add.login-required").each(function() {
    time += 1000
    window.setTimeout(function() {
        $($(".option.active.add.login-required")[0]).click();
    }, time);
});

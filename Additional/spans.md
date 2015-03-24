<div class="container">
    <div class="row">
		<div class="col-md-8">
			<div class="panel panel-default">
				<div class="panel-heading">
					<h3 class="panel-title">Panel 1</h3>
					<span class="pull-right clickable"><i class="glyphicon glyphicon-chevron-up"></i></span>
				</div>
				<div class="panel-body">
                    Founded in 1892 and headquartered in Fairfield, CT, LexisNexis Corporate Affiliations 
                    is a technology and financial services company. 
                    The company offers products and services ranging from aircraft engines, power generation, 
                    water processing, and household appliances, among others. 
                    It operates in business segments including Energy Infrastructure, Aviation, Healthcare, 
                    Transportation, Home & Business Solutions, and GE Capital. 
                    The company also provides medical imaging, business and consumer financing, 
                    and industrial products. 
                    It has presence in North America, Europe, Asia, South America, and Africa. 
                    According to the company's current 10K government filing it had FYE 12/31/2011 revenue of 
                    $147.3 billion and has 301,000 employees.
				</div>
			</div>
		</div>
		<div class="col-md-4">
			<div class="panel panel-default">
				<div class="panel-heading">
					<h3 class="panel-title">Panel 2</h3>
					<span class="pull-right clickable"><i class="glyphicon glyphicon-chevron-up"></i></span>
				</div>
				<div class="panel-body">
                    LexisNexis Corporate Affiliations<br />
                    121 Chanlon Road,<br /> 
                    South Building – First Floor,<br />
                    New Providence, NJ 07974<br />
                    phone: 800.340.3244
				</div>
		    </div>
	    </div>
	</div>
</div>

<style>
.panel-heading span {
    margin-top: -20px;
    font-size: 15px;
}
.row {
    margin-top: 40px;
    padding: 0 10px;
}
.clickable {
    cursor: pointer;
}    
</style>

<script type="text/javascript">
    jQuery(function ($) {
        $('.panel-heading span.clickable').on("click", function (e) {
            if ($(this).hasClass('panel-collapsed')) {
                // expand the panel
                $(this).parents('.panel').find('.panel-body').slideDown();
                $(this).removeClass('panel-collapsed');
                $(this).find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
            }
            else {
                // collapse the panel
                $(this).parents('.panel').find('.panel-body').slideUp();
                $(this).addClass('panel-collapsed');
                $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
            }
        });
    });
</script>

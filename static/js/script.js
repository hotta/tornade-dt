$(document).ready( function () {

	$('#myTable').DataTable({
		'paging'	  : true,
		'pageLength'  : 5,
		'lengthChange': false,
		'searching'   : true,
		'ordering'	: true,
		'info'		: true,
		'autoWidth'   : true,
		"scrollCollapse": true,
		'scrollX'	 : true,
		'scrollY'	 : '185px',
		'tabIndex'	: -1,
		'order'	   : [[ 0, 'asc' ]],
		'colReorder'  : true,
		'serverSide'  : false,      /* 今回から false に */
		'ajax'		: {
			'url'  : '/init',
			'type' : 'POST',
			'data' : function ( d ) {
				d.searchName = $("#searchName").val();
			}
		},
		'columns'	 : [
			{ 'data' : 'no', width: 40 },
			{ 'data' : 'name', width: 60  },
			{ 'data' : 'sex', width: 40  },
			{ 'data' : 'age', width: 40  },
			{ 'data' : 'kind_name', width: 100  },
			{ 'data' : 'favorite', width: 120  },
		],
		'language'   : {
			'decimal':		".",
			'emptyTable':	 "表示するデータがありません。",
			'info':		   "_START_ ～ _END_ / _TOTAL_ 件中",
			'infoEmpty':	  "0 ～ 0 / 0 件",
			'infoFiltered':   "(合計 _MAX_ 件からフィルタリングしています)",
			'infoPostFix':	"",
			'thousands':	  ",",
			'lengthMenu':	 "1ページ _MENU_ 件を表示する",
			'loadingRecords': "読み込み中...",
			'processing':	 "処理中...",
			'search':		 "絞り込み:",
			'zeroRecords':	"一致するデータが見つかりません。",
			'paginate': {
				'first':	  "最初",
				'last':	   "最後",
				'next':	   "次",
				'previous':   "前"
			}
		}
	});

	$("#searchButton").on("click", function() {
		$('#myTable').DataTable().ajax.url("/search").load();
		$('#myTable').DataTable().ajax.reload();
	})

} );
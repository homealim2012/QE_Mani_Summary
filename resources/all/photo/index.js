/**
 *
 * @authors ffftzh (ffftzh@gmail.com)
 * @date    2016-08-06 13:58:43
 * @version 1.0
 */

// var _$ = function(selector){
//     var result = null;
//     if(document.querySelectorAll){
//         result = document.querySelectorAll(selector);
//         if(result.length==1){
//             result = result[0];
//         }
//         return result;
//     }
//     console.error("当前浏览器不支持querySelectorAll！");
// }

(function () {
    var time = 0;

    function ImageGallery(option) {
        this.nowPageIndex = 0;
        this.nowImgIndex = 0;
        this.page_width = 250;
        this.page_height = 200;
        this.pageNum_w = 0;
        this.pageNum_h = 0;
        this.pageNum = 0;
        this.rootElement = $(option["Id"])[0];
        this.container = null;
        this.popLayer = null;
        this.imageList = option["imglist"];
        this.init();
    }

    ImageGallery.prototype = {
        init: function () {
            this.rootElement.className += " image-gallery";

            this.container = document.createElement("div");
            this.container.className = "photo-container";
            this.rootElement.appendChild(this.container);

            this.popLayer = document.createElement("div");
            this.popLayer.className = "popLayer hidden";

            var left = document.createElement("div");
            left.className = "left-array";
            this.popLayer.appendChild(left);

            var right = document.createElement("div");
            right.className = "right-array";
            this.popLayer.appendChild(right);

            var close = document.createElement("div");
            close.className = "close-button";
            close.innerHTML = "+";
            this.popLayer.appendChild(close);

            document.body.appendChild(this.popLayer);


            this.resize();
            this.fillPage();
            this.bound_event();
        },
        resize: function () {
            var root_width = this.rootElement.clientWidth;
            var root_height = this.rootElement.clientHeight;

            this.pageNum_w = Math.round(root_width / this.page_width);
            this.pageNum_h = Math.round(root_height / this.page_height);
            this.pageNum = Math.ceil(this.imageList.length / (this.pageNum_h * this.pageNum_w));
            console.log(this.pageNum_w, this.pageNum_h, this.pageNum)
        },

        fillPage: function () {
            this.container.style.width = "100%";
            var content = "";
            for (var i = 0; i < this.pageNum; i++) {
                content += this.generate_page(i);
            }
            this.container.innerHTML = content;
            this.render(0);

        },

        generate_page: function (index) {
            var pageElem = "<div class = 'photo-page right-slideOut' style = 'width:" + 100 + "%;'>";
            var start = index * this.pageNum_h * this.pageNum_w;
            var end = start + this.pageNum_h * this.pageNum_w;
            if (end > this.imageList.length) {
                end = this.imageList.length;
            }


            for (var i = start; i < end; i++) {
                pageElem += "<div class = 'postcard' data-index='" + i + "' data-img='"
                    + this.imageList[i] + "' style = 'width:" + (80 / this.pageNum_w)
                    + "%;height:" + (80 / this.pageNum_h) + "%;'></div>";
            }
            // for(var i=start;i<end;i++){
            //     pageElem += "<div class = 'postcard' data-index='"+i+"' data-img='"
            //         +this.imageList[i]+"' style = 'width:"+ (80/this.pageNum_w)
            //         +"%;height:"+(80/this.pageNum_h)+"%;margin:"+(10/this.pageNum_w)+"% "
            //         +(10/this.pageNum_w)+"%;'></div>";
            // }
            pageElem += "</div>";
            return pageElem;
        },

        bound_event: function () {
            var self = this;
            document.addEventListener("wheel", function (ev) {
                if (ev.deltaY == 0) {
                    return;
                }
                process_move(ev.deltaY > 0 ? 1 : -1);
            });

            window.addEventListener("resize", function (ev) {
                self.resize();
                self.fillPage();
            });

            document.addEventListener("keydown", function (ev) {
                if (ev.keyCode == 37) {
                    process_move(-1);
                } else {
                    process_move(1);
                }
            });

            function process_move(flag) {
                if ((new Date()).getTime() - time < 500) {
                    return;
                }
                time = (new Date()).getTime();
                if (flag > 0 && self.nowPageIndex == self.pageNum - 1) {
                    return;
                } else if (flag < 0 && self.nowPageIndex == 0) {
                    return;
                }
                self.render(flag);
            }

            // this.popLayer.addEventListener("click",function(ev){
            //     if(ev.target.className == "close-button"){
            //         self.popLayer.className = "popLayer hidden";
            //         document.body.removeChild($(".pop-item")[0]);
            //     }else if(ev.target.className == "left-array"){
            //         self.generate_popLayer_content(1);
            //     }else if(ev.target.className == "right-array"){
            //         self.generate_popLayer_content(-1);
            //     }
            // });
            //
            // this.container.addEventListener("click",function(ev){
            //     if(ev.target.className!="postcard"){
            //         return;
            //     }
            //     self.popLayer.className = "popLayer";
            //     self.generate_popLayer_content(0,parseInt(ev.target.getAttribute("data-index")));
            // });
        },

        generate_popLayer_content: function (flag, imgIndex) {
            // if((new Date()).getTime()-time<500){
            //     return;
            // }
            // time = (new Date()).getTime();
            if ((flag == 1 && this.nowImgIndex == 0) || (flag == -1 && this.nowImgIndex == this.imageList.length - 1)) {
                return null;
            }
            var genele = document.createElement("div");
            genele.className = "pop-item now-show";


            if (imgIndex != null) {
                this.nowImgIndex = imgIndex;
            } else {
                this.nowImgIndex -= flag;
                if (flag == -1) {
                    genele.className += " pop-left";
                } else {
                    genele.className += " pop-right";
                }
            }

            var nowShow = $(".now-show")[0];
            genele.style.backgroundImage = "url(" + this.imglist[this.nowImgIndex] + ")";
            document.body.appendChild(genele);
            if (imgIndex == null) {
                if (flag == -1) {
                    nowShow.className = "pop-item out-left";
                } else {
                    nowShow.className = "pop-item out-right";
                }
                setTimeout(function () {
                    document.body.removeChild(nowShow);
                }, 350);
            }

        },

        render: function (flag) {
            var kf = flag;
            if (flag == -1) {
                flag = 0;
            }
            var slidein_class = [" left-slideIn", " right-slideIn"];
            var slideout_class = [" left-slideOut", " right-slideOut"];
            // this.container.style.left = -(this.nowPageIndex*this.rootElement.clientWidth)+"px";
            var pagelist = $(".image-gallery>.photo-container>.photo-page");
            pagelist[this.nowPageIndex].className = "photo-page";
            pagelist[this.nowPageIndex].className += slideout_class[1 - flag];

            pagelist[this.nowPageIndex + kf].className = "photo-page";
            pagelist[this.nowPageIndex + kf].className += slidein_class[flag];
            this.nowPageIndex += kf;
            var self = this;
            setTimeout(function () {
                $(($(self.rootElement).find(".photo-page"))[self.nowPageIndex]).find(".postcard").each(function () {
                    this.style.backgroundImage = "url(" + this.getAttribute("data-img") + ")";
                });
            }, 1000);

        }
    }
    window.ImageGallery = ImageGallery;
})();

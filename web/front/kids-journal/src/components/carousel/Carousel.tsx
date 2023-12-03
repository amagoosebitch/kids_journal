import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Carousel.css";

import Slider from "react-slick";
import { useState } from "react";

import {infoGroups} from "../../const";

export type CarouselProps = {
  carouselLabel: string;
  carouselAge: string;
  carouselAction?: [
    { carouselActionTitle: string; carouselActionCategory: string },
  ];
};


export const Carousel = () => {
  let settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 3,
    initialSlide: 0,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 3,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          initialSlide: 2,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  const [carousels, setCarousels] = useState(infoGroups);
  return (
    <div className="carousel">
      <Slider {...settings}>
        {carousels.map((carousel) => (
          <div className="carousel_box">
            <div className="carousel_box-title">
              <div className="carousel_box-name">Группа {carousel.carouselLabel}</div>
              <div className="carousel_box-age">{carousel.carouselAge}</div>
            </div>
            {carousel.carouselAction.map((action) => (
              <div
                className={`carousel_box-action ${
                  action.carouselActionCategory === "1" ? "isOrange" : "isGreen"
                }`}
              >
                {action.carouselActionTitle}
              </div>
            ))}
          </div>
        ))}
      </Slider>
    </div>
  );
};

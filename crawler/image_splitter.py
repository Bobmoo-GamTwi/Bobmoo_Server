from __future__ import annotations
import os
from typing import List, Tuple
from PIL import Image
from pdf2image import convert_from_path

class ImageSplitter:
    def _ensure_dir(self, path: str) -> None:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    def convert_pdf_to_image(self, pdf_path: str, output_dir: str) -> str:
        self._ensure_dir(output_dir)
        print(f"🔄 PDF를 이미지로 변환 중... ({pdf_path})")

        # 🚨 여기에 아까 압축 푼 poppler의 'bin' 폴더 경로를 정확히 적어줘!
        # 주의: 경로 앞에 r 을 꼭 붙여야 해 (Raw String)
        poppler_dir = r"C:\poppler\Library\bin" # 압축 푼 형태에 따라 C:\poppler\bin 일 수도 있어!

        # poppler_path 파라미터를 추가해서 변환!
        images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_dir)

        img_path = os.path.join(output_dir, 'full_menu_temp.png')
        images[0].save(img_path, 'PNG')
        return img_path

    def crop_and_compose(
            self,
            input_image_path: str,
            output_dir: str,
            left_margin_ratio: float = 0.018,
            right_margin_ratio: float = 0.018,
            top_margin_ratio: float = 0.072,
            bottom_margin_ratio: float = 0.12,
            col_ratios: List[float] | None = None,
            background_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> List[str]:

        if col_ratios is None:
            col_ratios = [0.125] * 8

        img = Image.open(input_image_path)
        width, height = img.size

        # 여백 제거
        left = int(width * left_margin_ratio)
        right = width - int(width * right_margin_ratio)
        top = int(height * top_margin_ratio)
        bottom = height - int(height * bottom_margin_ratio)

        crop_width = right - left
        crop_height = bottom - top

        # 열 단위 크롭
        columns: List[Image.Image] = []
        acc = 0.0
        for ratio in col_ratios:
            x = left + int(acc * crop_width)
            w = int(ratio * crop_width)
            y = top
            h = crop_height
            col_img = img.crop((x, y, x + w, y + h))
            columns.append(col_img)
            acc += ratio

        # 구분 기둥(0번째 인덱스)
        legend_col = columns[0]
        out_paths: List[str] = []
        self._ensure_dir(output_dir)

        day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        for day_idx, day_col in enumerate(columns[1:8]):
            composed_width = legend_col.width + day_col.width
            composed_height = max(legend_col.height, day_col.height)

            canvas = Image.new("RGB", (composed_width, composed_height), background_color)
            canvas.paste(legend_col, (0, 0))
            canvas.paste(day_col, (legend_col.width, 0))

            out_name = f"{day_names[day_idx]}.png"
            out_path = os.path.join(output_dir, out_name)
            canvas.save(out_path)
            out_paths.append(out_path)

        print(f"✂️ 이미지 7등분 및 합성 완료: {output_dir}")
        return out_paths
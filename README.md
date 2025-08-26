# vision_segmentation
분할 알고리즘 구현
밝기값 기반으로 이미지를 분할하는 과정을 진행했습니다.
처음에는 불필요한 선들이 많이 잡혔는데, 예를 들어 Bed가 검출되거나 이미지 상단의 불필요한 선들이 포함되는 문제가 있었습니다.
이를 해결하려고 Y축 기준선을 설정해 특정 범위 이하의 선들을 제거했지만, 이 방식은 우리가 원했던 몸통 부분까지 같이 제거되는 문제가 있었습니다.

그래서 최종적으로 이미지 중앙에 위치한 물체만 검출되도록 코드를 수정했습니다.

input -> output -> overlay
<img width="1552" height="519" alt="image" src="https://github.com/user-attachments/assets/b39bbaf1-f00a-42da-8a72-77e1fcbaf795" />

<프로세스 순서도>
<img width="660" height="1317" alt="image" src="https://github.com/user-attachments/assets/63e70a63-55ef-4995-b0ed-032f56949e42" />




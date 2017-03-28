/**
 * @file test_akaze_features_port.cpp
 * @brief Main program for testing OpenCV A-KAZE port
 * @date May 24, 2014
 * @author Pablo F. Alcantarilla
 */

#include "./src/utils.h"

// System
#include <string>
#include <vector>
#include <iostream>

using namespace std;
using namespace cv;

float value_akaze(string s1, string s2) {
  cv::Mat img1;
  cv::Mat img2;

  // Open the input image
  img1 = imread(s1, 1);
  img2 = imread(s2, 1);

  // Create KAZE object
  Ptr<Feature2D> dakaze1 = AKAZE::create();
  Ptr<Feature2D> dakaze2 = AKAZE::create();

  // Detect A-KAZE features in the input image
  vector<cv::KeyPoint> kpts1, kpts2;
  cv::Mat desc1;
  cv::Mat desc2;

  dakaze1->detectAndCompute(img1, cv::noArray(), kpts1, desc1, false);
  dakaze2->detectAndCompute(img2, cv::noArray(), kpts2, desc2, false);

  draw_keypoints(img1, kpts1);
  draw_keypoints(img2, kpts2);

  // Match
  vector< vector<cv::DMatch> > knnmatch_points;
  cv::BFMatcher match(cv::NORM_HAMMING);
  match.knnMatch(desc1, desc2, knnmatch_points, 2);
  const double match_par = 0.6;
  vector<cv::DMatch> goodMatch;

  //KeyPoint -> Point2d
  vector<cv::Point2f> match_point1;
  vector<cv::Point2f> match_point2;
  for (size_t i = 0; i < knnmatch_points.size(); ++i) {
    double distance1 = knnmatch_points[i][0].distance;
    double distance2 = knnmatch_points[i][1].distance;
    if (distance1 <= distance2 * match_par) {
      goodMatch.push_back(knnmatch_points[i][0]);
      match_point1.push_back(kpts1[knnmatch_points[i][0].queryIdx].pt);
      match_point2.push_back(kpts2[knnmatch_points[i][0].trainIdx].pt);
    }
  }

  return (float)match_point1.size() / (float)kpts1.size();
  // homography matrix
  // cv::Mat masks;
  // cv::Mat H = cv::findHomography(match_point1, match_point2, masks, cv::RANSAC, 3);
  // cout << H << endl;

  // Show the detected A-KAZE features
  // cv::imshow("A-KAZE", img1);
  // cv::imshow("T_A-KAZE", img2);
  // cv::waitKey(1);

  // int nr_kpts = kpts1.size();

  // cout << "A-KAZE Results" << endl;
  // cout << "********************" << endl;
  // cout << "# Keypoints:    \t" << nr_kpts << endl;
  // cout << endl;
}


/* ************************************************************************* */
int main(int argc, char *argv[]) {
  cout << value_akaze(argv[1], argv[2]) << endl;
  return 0;
}

